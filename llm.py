import os
import sys
from dotenv import load_dotenv

# Error handling untuk import modul
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    print("Error: Modul 'langchain-google-genai' tidak ditemukan.")
    print("Silakan instal dengan: pip install langchain-google-genai")
    sys.exit(1)

def initialize_llm():
    try:
        # 1. Load environment variables
        load_dotenv()
        
        # 2. Ambil dan validasi API Key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY tidak ditemukan di file .env atau environment variable.")

        # 3. Inisialisasi Model
        # Dibungkus dalam try-except untuk menangkap error konfigurasi
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=api_key, 
            temperature=0
        )
        
        print("Berhasil menginisialisasi LLM.")
        return llm

    except ValueError as ve:
        print(f"Kesalahan Konfigurasi: {ve}")
    except Exception as e:
        # Menangkap error tidak terduga lainnya (misal: masalah jaringan saat init)
        print(f"Terjadi kesalahan yang tidak terduga: {e}")
    
    return None

# Eksekusi
if __name__ == "__main__":
    llm = initialize_llm()
    
    if llm:
        # Contoh penggunaan dengan error handling tambahan saat pemanggilan
        try:
            # response = llm.invoke("Halo, apa kabar?")
            # print(response.content)
            pass
        except Exception as api_error:
            print(f"Gagal memanggil API Gemini: {api_error}")