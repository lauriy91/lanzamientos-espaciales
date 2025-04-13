import subprocess
import sys
import os

def install_aws_cdk():
    # Instalar aws-cdk-lib
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aws-cdk-lib==2.108.1"])
    
    # Instalar constructs
    subprocess.check_call([sys.executable, "-m", "pip", "install", "constructs==10.3.0"])
    
    # Verificar si npm está instalado
    try:
        subprocess.check_call(["npm", "--version"])
        # Instalar AWS CDK globalmente
        subprocess.check_call(["npm", "install", "-g", "aws-cdk"])
        print("AWS CDK CLI instalado globalmente.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("npm no encontrado. Por favor, instala Node.js y npm para usar AWS CDK CLI.")
    
    print("Instalación completada.")

if __name__ == "__main__":
    install_aws_cdk() 