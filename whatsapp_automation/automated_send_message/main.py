import pywhatkit  # type: ignore

numbers = ["+923072009835", "+923142249632"]
message = """
Assalam-o-Alaikum!
Main Huzaifa Mukhtar bol raha hoon.

Hum local shops aur businesses ke liye professional websites banate hain jo aapke business ko online grow karne mein help karti hain — design, development, SEO, sab kuch ek hi jagah par.

Apni website se aap:
✅ Zyada customers tak online pohonch sakte hain
✅ Apni brand ki pehchan aur reputation barha sakte hain
✅ Online orders ya inquiries lena shuru kar sakte hain
✅ Apna business 24/7 online showcase kar sakte hain

Filhaal special offer chal raha hai!
Agar aap interested hain ya details chahte hain, to WhatsApp ya call par rabta karein:
📞 03072009835

Main aapko free mein design samples aur idea bhej sakta hoon taake aap aram se decision le saken.

Shukriya! Aapka response ka intezar rahega. 😊   
"""

delay_between_messages = 10  # adjust if needed
for number in numbers:
    pywhatkit.sendwhatmsg_instantly(
        phone_no=number,
        message=message,
        wait_time=10,  # seconds to wait for the web to load
        # tab_close=True,  # close the tab after sending
    )

print(f"Message sent to {number}")
