import subprocess
import pathlib
import tempfile

RVC_ROOT = pathlib.Path(r"C:\RVC\RVC-WebUI")
RVC_PYTHON = RVC_ROOT / "python" / "python.exe"  # adjust if different
INFER_SCRIPT = RVC_ROOT / "infer_cli.py"
WEIGHTS_DIR = RVC_ROOT / "weights"
INDEX_DIR = RVC_ROOT / "logs"


class RVCClient:
    """Client for RVC (Retrieval-based Voice Conversion)"""
    
    def __init__(self, options=None):
        self.options = options or {}
        self.rvc_root = RVC_ROOT
        self.rvc_python = RVC_PYTHON
        self.infer_script = INFER_SCRIPT
        self.weights_dir = WEIGHTS_DIR
        self.index_dir = INDEX_DIR
    
    def convert_voice(
        self,
        input_wav: pathlib.Path,
        model_name: str,
        index_name: str | None = None,
        f0_up_key: int = 0,
    ) -> pathlib.Path:
        """Convert voice using RVC model"""
        input_wav = pathlib.Path(input_wav)
        tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix="rvc_out_"))
        output_wav = tmp_dir / "converted.wav"

        index_path = ""
        if index_name:
            index_path = str(self.index_dir / index_name)

        cmd = [
            str(self.rvc_python),
            str(self.infer_script),
            "--model",
            model_name,
            "--input",
            str(input_wav),
            "--output",
            str(output_wav),
            "--f0_up_key",
            str(f0_up_key),
        ]
        
        if index_path:
            cmd += ["--index", index_path]

        subprocess.check_call(cmd, cwd=self.rvc_root)
        return output_wav


def convert_voice_with_rvc(
    input_wav: pathlib.Path,
    model_name: str,
    index_name: str | None = None,
    f0_up_key: int = 0,
) -> pathlib.Path:
    """Legacy function - wraps RVCClient for backward compatibility"""
    client = RVCClient()
    return client.convert_voice(input_wav, model_name, index_name, f0_up_key)

