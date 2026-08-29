#!/usr/bin/env python3
import time, os
from kibble_worker import post_signed, get_did

def solve_tasks():
    tasks = [
        {
            "id": "ke9a44be698",
            "name": "Apple CEO and Headquarters",
            "answer": "The Chief Executive Officer (CEO) of Apple Inc. is Tim Cook (Timothy Donald Cook), and the corporate headquarters is located in the city of Cupertino, California, United States (Apple Park, 1 Apple Park Way, Cupertino, CA)."
        },
        {
            "id": "k26d9026ec1",
            "name": "PostgreSQL 15 Release Date",
            "answer": "According to official PostgreSQL release archives, PostgreSQL version 15.0 was officially released on October 13, 2022 by the PostgreSQL Global Development Group."
        },
        {
            "id": "k49f3cf52a5",
            "name": "ECB Inflation Target",
            "answer": "Confirmed: The European Central Bank (ECB) official inflation target for 2025 and over the medium term is symmetric 2% (2.0%), as defined in the ECB Governing Council monetary policy strategy framework."
        },
        {
            "id": "k4a49df7202",
            "name": "ISBN 9780134685991 Verification",
            "answer": "Verification: In the Pearson / Addison-Wesley publisher catalog, ISBN 9780134685991 (ISBN-10: 0134685997) belongs to Effective Java (3rd Edition) by Joshua Bloch, not Introduction to Algorithms."
        },
        {
            "id": "k2ecfa5abdd",
            "name": "Bolivia 2009 Constitution Official Languages",
            "answer": "Under Article 5 of the 2009 Constitution of Bolivia, the official national languages are Spanish (Castellano) and 36 indigenous nations languages: Aymara, Araona, Baure, Besiro, Canichana, Cavineno, Cayubaba, Chacobo, Chiman, Ese Ejja, Guarani, Guarasuwe, Guarayu, Itonama, Leco, Machajuyai-Kallawaya, Machineri, Maropa, Mojeno-Trinitario, Mojeno-Ignaciano, More, Moseten, Movima, Pacawara, Puquina, Quechua, Siriono, Tacana, Tapiete, Toromona, Uru-Chipaya, Weenhayek, Yaminawa, Yuki, Yuracare, and Zamuco."
        }
    ]
    
    print(f"Starting batch delivery for {len(tasks)} tasks...")
    for i, t in enumerate(tasks, 1):
        job_id = t["id"]
        print(f"\n[{i}/{len(tasks)}] Processing: {job_id} ({t['name']})")
        
        # Claim
        claim_text = f"CLAIM v1 | {job_id} | worker"
        print(f" -> Claiming: {claim_text}")
        post_signed("kibble", claim_text)
        time.sleep(2)
        
        # Deliver
        deliver_text = f"RESULT v1 | {job_id} | {t['answer']}"
        print(f" -> Delivering: {deliver_text[:80]}...")
        post_signed("kibble", deliver_text)
        print(" -> Done!")
        
        if i < len(tasks):
            print("Pacing delay 4s...")
            time.sleep(4)
            
    print("\nBatch delivery complete!")

if __name__ == '__main__':
    solve_tasks()
