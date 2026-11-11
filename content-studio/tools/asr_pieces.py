import sys, re, glob, wave, subprocess, numpy as np, sherpa_onnx
src=sys.argv[1]; wavf=sys.argv[2]; outf=sys.argv[3]
d='/tmp/claude-0/-home-user/07de6378-c75c-50a4-a4d1-5b89e5e49d3a/scratchpad/asr/sherpa-onnx-whisper-small/'
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=glob.glob(d+'*encoder*.int8.onnx')[0],decoder=glob.glob(d+'*decoder*.int8.onnx')[0],tokens=glob.glob(d+'*tokens.txt')[0],language='id',task='transcribe',num_threads=4)
w=wave.open(wavf); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
out=subprocess.run(['ffmpeg','-i',src,'-af','silencedetect=noise=-35dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
ss=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]; se=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
vo=[];prev=0.0
for s0,e0 in zip(ss,se):
    if s0-prev>0.3: vo.append((prev,s0))
    prev=e0
vo.append((prev,len(a)/16000))
f=open(outf,'w')
for a0,b0 in vo:
    pad=0.15
    s=r.create_stream(); seg=a[max(0,int((a0-pad)*16000)):int((b0+pad)*16000)]
    seg=np.concatenate([np.zeros(4000,dtype=np.float32),seg,np.zeros(4000,dtype=np.float32)])
    s.accept_waveform(16000,seg); r.decode_stream(s)
    f.write('%.2f-%.2f | %s\n'%(a0,b0,s.result.text.strip())); f.flush()
f.close()
