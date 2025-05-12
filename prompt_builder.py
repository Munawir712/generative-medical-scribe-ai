def build_cppt_prompt(user_input: str) -> str:
    template = """
    Anda adalah Asisten Medis Digital yang ahli dalam membuat catatan CPPT (Catatan Perkembangan Pasien Terintegrasi).
    Buat catatan CPPT yang lengkap dan terstruktur berdasarkan input dokter berikut.
    Berikan output dalam format JSON dengan struktur berikut:

    Input Dokter:
    "{input}"

    Output harus dalam format JSON dengan struktur berikut:
    {{
        "data": {{
            "subject": "Keluhan utama dalam string",
            "object": "Deskripsi gejala dalam string",
            "assessment": "Diagnosis dalam string",
            "plan": "Rencana tindakan dalam string",
            "instruction": "Instruksi pasien dalam string",
            "evaluation": "Evaluasi dalam string",
            "rekom_diagnosa_utama": [
                {
                    "code_icd": "Kode ICD-10",
                    "diagnosa": "Nama diagnosa"
                }
            ],
            "rekom_prosedur_utama": [
                {
                    "code_icd": "Kode ICD-9-CM",
                    "diagnosa": "Nama prosedur"
                }
            ]
        }}
    }}

    Catatan:
    1. Gunakan format string untuk semua field utama (subject, object, assessment, plan, instruction, evaluation)
    2. Untuk rekom_diagnosa_utama dan rekom_prosedur_utama, gunakan array of objects
    3. Gunakan kode ICD-10 yang valid untuk diagnosa
    4. Gunakan kode ICD-9-CM yang valid untuk prosedur
    5. Sertakan minimal 2 diagnosa dan 2 prosedur
    6. Buat output dalam format JSON yang valid
    7. Jangan tambahkan komentar atau penjelasan lain dalam output
    8. Ikuti contoh format yang diberikan
    """
    return template.replace("{input}", user_input)
