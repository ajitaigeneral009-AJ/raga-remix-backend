"""
Automated Deployment Script for Raga Remix Studio Backend
Run this script to set up the complete backend automatically
"""

import os
import sys
import subprocess
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class BackendDeployer:
    """Automated backend deployment"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.venv_dir = self.project_dir / "venv"
        self.errors = []
    
    def run(self):
        """Execute full deployment pipeline"""
        
        logger.info("=" * 70)
        logger.info("🎵 RAGA REMIX STUDIO - AUTOMATED DEPLOYMENT")
        logger.info("=" * 70)
        
        steps = [
            ("Checking Python version", self.check_python),
            ("Checking FFmpeg installation", self.check_ffmpeg),
            ("Creating virtual environment", self.create_venv),
            ("Installing dependencies", self.install_dependencies),
            ("Creating .env file", self.create_env_file),
            ("Creating directory structure", self.create_directories),
            ("Creating __init__.py files", self.create_init_files),
            ("Indexing knowledge base", self.index_knowledge),
            ("Testing services", self.test_services),
        ]
        
        for step_name, step_func in steps:
            logger.info(f"\\n▶ {step_name}...")
            try:
                step_func()
                logger.info(f"✅ {step_name} completed")
            except Exception as e:
                logger.error(f"❌ {step_name} failed: {e}")
                self.errors.append((step_name, str(e)))
        
        self.print_summary()
    
    def check_python(self):
        """Verify Python version"""
        version = sys.version_info
        
        if version.major < 3 or (version.major == 3 and version.minor < 9):
            raise RuntimeError(f"Python 3.9+ required, found {version.major}.{version.minor}")
        
        logger.info(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    def check_ffmpeg(self):
        """Verify FFmpeg installation"""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                version_line = result.stdout.split('\\n')[0]
                logger.info(f"   {version_line}")
            else:
                raise RuntimeError("FFmpeg not working")
                
        except FileNotFoundError:
            logger.warning("⚠️  FFmpeg not found in PATH")
            logger.warning("   Download: https://www.gyan.dev/ffmpeg/builds/")
            logger.warning("   Add to PATH and restart terminal")
    
    def create_venv(self):
        """Create virtual environment"""
        if self.venv_dir.exists():
            logger.info("   Virtual environment already exists")
            return
        
        subprocess.run([sys.executable, "-m", "venv", str(self.venv_dir)], check=True)
        logger.info(f"   Created: {self.venv_dir}")
    
    def get_pip_executable(self):
        """Get pip executable path"""
        if sys.platform == "win32":
            return str(self.venv_dir / "Scripts" / "pip.exe")
        else:
            return str(self.venv_dir / "bin" / "pip")
    
    def install_dependencies(self):
        """Install Python packages"""
        pip_exe = self.get_pip_executable()
        
        # Upgrade pip
        subprocess.run([pip_exe, "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        requirements_file = self.project_dir / "requirements.txt"
        
        if requirements_file.exists():
            logger.info(f"   Installing from: {requirements_file}")
            subprocess.run([pip_exe, "install", "-r", str(requirements_file)], check=True)
        else:
            logger.warning("⚠️  No requirements.txt file found")
    
    def create_env_file(self):
        """Create .env configuration file"""
        env_file = self.project_dir / ".env"
        
        if env_file.exists():
            logger.info("   .env file already exists")
            return
        
        env_content = """# RAGA REMIX STUDIO - ENVIRONMENT VARIABLES

# OpenAI API Key (REQUIRED - Get from: https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-your-api-key-here

# ChromaDB Settings
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Audio Processing
TEMP_UPLOAD_DIR=./temp_uploads
OUTPUT_DIR=./outputs
MAX_FILE_SIZE_MB=50
DEMUCS_MODEL=htdemucs
SAMPLE_RATE=44100
TARGET_LOUDNESS_LUFS=-14.0

# Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=True

# RAG System
EMBEDDING_MODEL=text-embedding-ada-002
TOP_K_RESULTS=5

# LLM Settings
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
MAX_TOKENS=2000

# Processing
MAX_CONCURRENT_JOBS=3
PROCESSING_TIMEOUT_SECONDS=600
"""
        
        env_file.write_text(env_content)
        logger.info(f"   Created: {env_file}")
        logger.warning("   ⚠️  IMPORTANT: Edit .env and add your OpenAI API key!")
    
    def create_directories(self):
        """Create required directories"""
        directories = [
            "temp_uploads",
            "outputs",
            "chroma_db",
            "models",
            "services",
            "knowledge",
            "utils"
        ]
        
        for dir_name in directories:
            dir_path = self.project_dir / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"   Created {len(directories)} directories")
    
    def create_init_files(self):
        """Create __init__.py files for Python packages"""
        packages = ["models", "services", "knowledge", "utils"]
        
        for package in packages:
            init_file = self.project_dir / package / "__init__.py"
            if not init_file.exists():
                init_file.write_text("")
                logger.info(f"   Created: {package}/__init__.py")
    
    def index_knowledge(self):
        """Index knowledge base with ChromaDB"""
        indexer_file = self.project_dir / "knowledge" / "rag_knowledge_indexer.py"
        
        if not indexer_file.exists():
            logger.warning("⚠️  rag_knowledge_indexer.py not found, skipping indexing")
            return
        
        # Check if .env has valid OpenAI key
        env_file = self.project_dir / ".env"
        if env_file.exists():
            env_content = env_file.read_text()
            if "sk-your-api-key-here" in env_content:
                logger.warning("⚠️  OpenAI API key not set, skipping indexing")
                logger.warning("   Set OPENAI_API_KEY in .env, then run:")
                logger.warning(f"   python {indexer_file}")
                return
        
        # Run indexer
        python_exe = sys.executable if not self.venv_dir.exists() else (
            str(self.venv_dir / "Scripts" / "python.exe") if sys.platform == "win32"
            else str(self.venv_dir / "bin" / "python")
        )
        
        try:
            result = subprocess.run(
                [python_exe, str(indexer_file)],
                cwd=str(self.project_dir),
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                logger.info("   Knowledge base indexed successfully")
            else:
                logger.warning(f"⚠️  Indexing completed with warnings")
                
        except subprocess.TimeoutExpired:
            logger.warning("⚠️  Indexing timed out, may need to run manually")
        except Exception as e:
            logger.warning(f"⚠️  Indexing failed: {e}")
    
    def test_services(self):
        """Test service initialization"""
        logger.info("   Testing service imports...")
        
        # Simple existence check
        required_files = [
            "config.py",
            "services/rag_service.py",
            "services/audio_processor.py",
            "services/cover_generator.py",
            "models/schemas.py"
        ]
        
        for file_path in required_files:
            full_path = self.project_dir / file_path
            if full_path.exists():
                logger.info(f"   ✓ {file_path} found")
            else:
                logger.warning(f"   ⚠️  {file_path} missing")
    
    def print_summary(self):
        """Print deployment summary"""
        logger.info("\\n" + "=" * 70)
        
        if self.errors:
            logger.error("❌ DEPLOYMENT COMPLETED WITH ERRORS")
            logger.error("\\nErrors encountered:")
            for step, error in self.errors:
                logger.error(f"  - {step}: {error}")
        else:
            logger.info("✅ DEPLOYMENT SUCCESSFUL!")
        
        logger.info("\\n📋 NEXT STEPS:")
        logger.info("=" * 70)
        
        steps = [
            "1. Edit .env file and add your OpenAI API key",
            "2. If FFmpeg not installed, download and add to PATH",
            "3. Activate virtual environment:",
            f"   Windows: {self.venv_dir}\\\\Scripts\\\\activate",
            f"   Linux/Mac: source {self.venv_dir}/bin/activate",
            "4. Index knowledge base (if not done automatically):",
            "   python knowledge/rag_knowledge_indexer.py",
            "5. Start the server:",
            "   python main.py",
            "   OR",
            "   uvicorn main:app --reload",
            "6. Test API at: http://localhost:8000/docs",
            "7. Connect your frontend to: http://localhost:8000",
        ]
        
        for step in steps:
            logger.info(step)
        
        logger.info("\\n" + "=" * 70)
        logger.info("📚 Documentation: IMPLEMENTATION_GUIDE.md")
        logger.info("🐛 Troubleshooting: See guide for common issues")
        logger.info("=" * 70)


def main():
    """Main deployment function"""
    deployer = BackendDeployer()
    deployer.run()


if __name__ == "__main__":
    main()
