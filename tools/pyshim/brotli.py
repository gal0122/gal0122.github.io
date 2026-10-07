"""Minimal stand-in for the `brotli` module (pip can't install it here).
Uses Node's built-in zlib Brotli so fontTools can read/write WOFF2."""
import subprocess

MODE_GENERIC, MODE_TEXT, MODE_FONT = 0, 1, 2
error = Exception
_JS = ("const z=require('zlib');const c=[];process.stdin.on('data',d=>c.push(d)).on('end',()=>{"
       "const b=Buffer.concat(c);const a=process.argv;let o;"
       "if(a[1]==='c'){o=z.brotliCompressSync(b,{params:{[z.constants.BROTLI_PARAM_MODE]:+a[2],"
       "[z.constants.BROTLI_PARAM_QUALITY]:+a[3],[z.constants.BROTLI_PARAM_SIZE_HINT]:b.length}});}"
       "else{o=z.brotliDecompressSync(b);}process.stdout.write(o);});")


def compress(data, mode=MODE_GENERIC, quality=11, lgwin=22, lgblock=0):
    return subprocess.run(['node', '-e', _JS, 'c', str(mode), str(quality)],
                          input=bytes(data), capture_output=True, check=True).stdout


def decompress(data):
    return subprocess.run(['node', '-e', _JS, 'd'], input=bytes(data), capture_output=True, check=True).stdout
