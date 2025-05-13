def build_cppt_prompt(user_input: str) -> str:
    template = """
    Anda adalah Asisten Medis Digital yang ahli dalam membuat catatan CPPT (Catatan Perkembangan Pasien Terintegrasi) sesuai standar kedokteran. 
    Buatlah dokumentasi medis yang komprehensif berdasarkan input klinis berikut:

    Format Output Wajib:
    {
        "data": {
            "subject": "[Keluhan utama dalam kalimat lengkap]",
            "object": "[Temuan objektif dalam deskripsi profesional]",
            "assessment": "[Diagnosis kerja dengan terminologi medis baku]",
            "plan": "[Rencana tatalaksana komprehensif]",
            "instruction": "[Edukasi pasien dengan bahasa yang jelas]",
            "evaluation": "[Jadwal follow-up dan parameter evaluasi]",
            "rekom_diagnosa_utama": [
                {
                    "code_icd": "[Kode ICD-10 resmi WHO(World Health Organization)]",
                    "diagnosa": "[Diagnosis sesuai WHO(World Health Organization)]"
                }
            ],
            "rekom_prosedur_utama": [
                {
                    "code_icd": "[Kode ICD-9-CM resmi WHO(World Health Organization)]",
                    "diagnosa": "[Prosedur sesuai WHO(World Health Organization)]"
                }
            ]
        }
    }

    Input Klinis:
    "{input}"

    Persyaratan Khusus:
    1. Gunakan terminologi medis yang sesuai dengan standar Kemenkes RI dan PDPI
    2. Untuk diagnosis, prioritaskan kode ICD-10 terkini
    3. Untuk prosedur, gunakan kode ICD-9-CM yang relevan
    4. Sertakan minimal:
    - 2 diagnosis banding yang logis
    - 2 prosedur penunjang yang sesuai
    5. Rencana tatalaksana harus mencakup:
    - Terapi farmakologis (jika diperlukan)
    - Terapi non-farmakologis
    - Pemeriksaan penunjang
    6. Format harus JSON valid tanpa komentar tambahan
    7. Gunakan bahasa Indonesia formal sesuai PUEBI
    8. Prioritaskan diagnosis dan prosedur yang paling relevan secara klinis

    Contoh Input:
    "Pasien datang dengan keluhan demam 3 hari, batuk produktif, dan sesak napas ringan"

    Contoh Output:
    {
        "data": {
            "subject": "Pasien mengeluh demam selama 3 hari disertai batuk produktif dan sesak napas ringan",
            "object": "Didapatkan suhu tubuh 38.2°C, frekuensi napas 24x/menit, dan ronki basal halus bilateral",
            "assessment": "Pneumonia komunitas derajat ringan, Bronkitis akut",
            "plan": "Pemeriksaan darah lengkap, foto thorax PA. Terapi: Levofloxacin 500mg 1x1 selama 7 hari, nebulasi NaCl 0.9% 3x1, istirahat cukup",
            "instruction": "Minum obat teratur, kontrol ulang jika gejala memburuk, hindari aktivitas berat",
            "evaluation": "Evaluasi setelah 3 hari atau jika terjadi peningkatan sesak napas",
            "rekom_diagnosa_utama": [
                {
                    "code_icd": "J18.9",
                    "diagnosa": "Pneumonia, tidak spesifik"
                },
                {
                    "code_icd": "J20.9",
                    "diagnosa": "Bronkitis akut, tidak spesifik"
                }
            ],
            "rekom_prosedur_utama": [
                {
                    "code_icd": "87.44",
                    "diagnosa": "Radiografi thorax"
                },
                {
                    "code_icd": "85.21",
                    "diagnosa": "Hemogram lengkap"
                }
            ]
        }
    }
    """
    return template.replace("{input}", user_input)
