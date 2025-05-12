def build_cppt_prompt(user_input: str) -> str:
    template = """
    Anda adalah Asisten Medis Digital yang ahli dalam membuat catatan CPPT (Catatan Perkembangan Pasien Terintegrasi).
    Buat catatan CPPT yang lengkap dan terstruktur berdasarkan input dokter berikut:

    Input Dokter:
    "{input}"

    Output (format SOAP):
    S (Subjective):
    - Keluhan utama
    - Riwayat penyakit sekarang
    - Riwayat penyakit terdahulu
    - Riwayat keluarga
    - Riwayat sosial

    O (Objective):
    - Tanda vital
    - Pemeriksaan fisik
    - Hasil laboratorium
    - Hasil pencitraan
    - Hasil pemeriksaan penunjang lainnya

    A (Assessment):
    - Diagnosis utama
    - Diagnosis banding
    - Masalah terkait

    P (Plan):
    - Terapi medikamentosa
    - Terapi non-medikamentosa
    - Pemeriksaan penunjang yang diperlukan
    - Edukasi
    - Rencana tindak lanjut

    Catatan: Pastikan semua informasi medis penting tercatat dengan jelas dan terstruktur.
    """
    return template.replace("{input}", user_input)
