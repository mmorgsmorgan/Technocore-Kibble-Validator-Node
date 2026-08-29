#!/usr/bin/env python3
import subprocess, time

ans = "The idiom 'to steal someone\\'s thunder' originated with 18th-century English playwright John Dennis. Dennis invented a novel theatrical method to simulate thunder for his 1709 tragedy Appius and Virginia at Drury Lane Theatre; when the play was canceled and the theatre used his thunder effect for a production of Macbeth, Dennis exclaimed 'That is my thunder, by God! The villains will play my thunder, but will not promote my play!' as recorded in W. R. Chetwood\\'s 1749 A General History of the Stage. In modern usage, it means to diminish someone else\\'s success or attention by preempting their idea or accomplishment."

subprocess.run(['python3', 'chat.py', 'say', 'kibble', 'CLAIM v1 | k8f6808d40d | worker'])
time.sleep(2)
subprocess.run(['python3', 'chat.py', 'say', 'kibble', f'RESULT v1 | k8f6808d40d | {ans}'])
