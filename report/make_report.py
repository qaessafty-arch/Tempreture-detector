from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

REPO = "/home/user/Tempreture-detector"
OUT = REPO + "/report/Temperature_Detector_Report.docx"
NAVY = RGBColor(0x14, 0x21, 0x3D)
GREY = RGBColor(0x4A, 0x55, 0x68)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
for side in ("left_margin", "right_margin"):
    setattr(sec, side, Cm(2.2))
sec.top_margin = sec.bottom_margin = Cm(2.0)

st = doc.styles["Normal"]
st.font.name = "Calibri"; st.font.size = Pt(11)
st.paragraph_format.space_after = Pt(6)
for name, size in (("Title", 24), ("Heading 1", 16), ("Heading 2", 13)):
    s = doc.styles[name]
    s.font.name = "Arial"; s.font.size = Pt(size); s.font.bold = True
    s.font.color.rgb = NAVY
    s.element.rPr.rFonts.set(qn("w:asciiTheme"), "") if False else None

# page numbers in footer
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run()
for t, txt in (("begin", None), (None, "PAGE"), ("end", None)):
    if t:
        e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), t); r._r.append(e)
    else:
        e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt; r._r.append(e)


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hexcolor)
    tcPr.append(sh)


def table(rows, widths=None):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.text = ""
            run = c.paragraphs[0].add_run(val)
            run.font.size = Pt(10)
            c.paragraphs[0].paragraph_format.space_after = Pt(0)
            if i == 0:
                run.bold = True; run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); shade(c, "14213D")
            elif i % 2 == 0:
                shade(c, "F3F4F7")
            if widths:
                c.width = Cm(widths[j])
            if i < len(rows) - 1:  # keep the table on one page
                c.paragraphs[0].paragraph_format.keep_with_next = True
    if widths:
        t.autofit = False
        grid = t._tbl.tblGrid
        for j, gc in enumerate(grid.findall(qn("w:gridCol"))):
            gc.set(qn("w:w"), str(int(widths[j] * 567)))
        for j, col in enumerate(t.columns):
            col.width = Cm(widths[j])
    doc.add_paragraph()
    return t


def para(text, bold_lead=None, italic=False, color=None):
    p = doc.add_paragraph()
    if bold_lead:
        p.add_run(bold_lead).bold = True
    r = p.add_run(text); r.italic = italic
    if color: r.font.color.rgb = color
    return p


def bullets(items, style="List Bullet"):
    for n, it in enumerate(items, 1):
        if style == "List Number":  # numbered by hand so each list restarts at 1
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.9); p.paragraph_format.first_line_indent = Cm(-0.6)
            p.paragraph_format.space_after = Pt(3)
            p.add_run(f"{n}.  ")
        else:
            p = doc.add_paragraph(style=style)
        if isinstance(it, tuple):
            p.add_run(it[0]).bold = True; p.add_run(it[1])
        else:
            p.add_run(it)


def figure(path, caption, width_cm):
    doc.add_picture(path, width=Cm(width_cm))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c = doc.add_paragraph(caption); c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.runs[0].italic = True; c.runs[0].font.size = Pt(10); c.runs[0].font.color.rgb = GREY


def code(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    pPr = p._p.get_or_add_pPr()
    sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), "F3F4F7"); pPr.append(sh)
    lines = text.rstrip("\n").split("\n")
    for i, ln in enumerate(lines):
        r = p.add_run(ln); r.font.name = "Courier New"; r.font.size = Pt(8.5)
        r._r.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Courier New")
        if i < len(lines) - 1:
            r.add_break()


def equation(text):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.font.name = "Cambria Math"; r.font.size = Pt(13); r.italic = True


# ---------------- Title page ----------------
for _ in range(5): doc.add_paragraph()
t = doc.add_paragraph("Temperature Detector with Three LED Indicators", style="Title")
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
s = doc.add_paragraph("Project Report"); s.alignment = WD_ALIGN_PARAGRAPH.CENTER
s.runs[0].font.size = Pt(16); s.runs[0].font.color.rgb = GREY
doc.add_paragraph()
c = doc.add_paragraph("Electrical Engineering – Computer and Control for Algorithms"); c.alignment = WD_ALIGN_PARAGRAPH.CENTER
c.runs[0].font.size = Pt(13)
for _ in range(3): doc.add_paragraph()
h = doc.add_paragraph(); h.alignment = WD_ALIGN_PARAGRAPH.CENTER
h.add_run("Prepared by").bold = True
for i, n in enumerate(["Qays Ibrahim", "Mosayab Aziz", "Sarwar Haji", "Lasf Waysi", "Muhamed Ghazi", "Hasan Ibrahim", "Rzgar Farsat"], 1):
    p = doc.add_paragraph(f"{i}. {n}"); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after = Pt(2)
doc.add_paragraph()
sp = doc.add_paragraph(); sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
sp.add_run("Supervisor: ").bold = True; sp.add_run("Goran Wnis")
dp = doc.add_paragraph(); dp.alignment = WD_ALIGN_PARAGRAPH.CENTER
dp.add_run("Date: ").bold = True; dp.add_run("[date]")
doc.add_page_break()

# ---------------- Abstract ----------------
doc.add_heading("Abstract", level=1)
para("We built a battery-powered detector that reads an LM35 temperature sensor with an Arduino UNO and lights one of three LEDs: "
     "blue at 20 °C or below, orange above 20 °C up to 40 °C, and red above 40 °C. The report covers the components, the system "
     "design, the circuit and wiring, the algorithm, the code and the test results.")

# ---------------- 1 ----------------
doc.add_heading("1. Introduction and objective", level=1)
para("The objective is to measure air temperature and show its range with one of three coloured LEDs, so that anyone can read the "
     "state at a glance. The project applies a basic control loop: sense, compare with set limits, act.")
table([["Temperature range", "LED on", "Arduino pin"],
       ["T ≤ 20 °C", "Blue", "D8"],
       ["20 °C < T ≤ 40 °C", "Orange", "D9"],
       ["T > 40 °C", "Red", "D10"]], [6, 4, 4])
para("Exactly 20 °C lights blue and exactly 40 °C lights orange. Only one LED is on at a time.")

# ---------------- 2 ----------------
doc.add_heading("2. Components", level=1)
para("All parts are standard laboratory stock; the only calculated value is the LED resistor (section 4).")
table([["#", "Component", "Qty", "Role"],
       ["1", "Arduino UNO (ATmega328P) + USB cable", "1", "Controller; USB is only needed to upload the code"],
       ["2", "LM35 temperature sensor (TO-92)", "1", "Analog output, 10 mV per °C, range −55 to 150 °C"],
       ["3", "Blue LED, 5 mm", "1", "On when T ≤ 20 °C"],
       ["4", "Orange LED, 5 mm", "1", "On when 20 < T ≤ 40 °C"],
       ["5", "Red LED, 5 mm", "1", "On when T > 40 °C"],
       ["6", "Resistor 220 Ω, ¼ W", "3", "Limits each LED's current"],
       ["7", "Breadboard", "1", "Holds the circuit"],
       ["8", "Jumper wires (male–male)", "~10", "Connections"],
       ["9", "9 V alkaline battery", "1", "Powers the detector without a computer"],
       ["10", "9 V battery snap connector with wire leads", "1", "Connects the battery to the circuit"],
       ["11", "Slide or toggle switch (SPST)", "1", "Turns the detector on and off"]], [0.8, 6.2, 1.2, 8.4])

# ---------------- 3 ----------------
doc.add_heading("3. System design", level=1)
para("The system has three blocks: the LM35 senses (input), the Arduino converts and compares (processing), and the LEDs indicate "
     "(output). A 9 V battery powers the board through its VIN pin, so the detector works on its own. The Serial Monitor on a PC is "
     "optional and only shows the measured value while USB is connected for testing.")
figure(REPO + "/diagrams/block_diagram.png", "Figure 1 – Block diagram", 16.5)
doc.add_heading("From sensor voltage to degrees", level=2)
para("The LM35 output rises 10 mV for every 1 °C. The Arduino's 10-bit ADC divides its 5 V reference into 1024 steps of about "
     "4.88 mV, so one step is about 0.49 °C. Combining the two:")
equation("T (°C) = (raw × 5000 mV / 1024) / (10 mV/°C) = raw × 500 / 1024")
table([["ADC reading (raw)", "Voltage", "Temperature", "LED"],
       ["41", "0.20 V", "20.0 °C", "Orange (just above 20)"],
       ["51", "0.25 V", "24.9 °C", "Orange"],
       ["82", "0.40 V", "40.0 °C", "Red (just above 40)"],
       ["103", "0.50 V", "50.3 °C", "Red"]], [3.6, 3, 3.4, 6.6])
para("Raw 41 gives 20.02 °C and raw 82 gives 40.04 °C, so both already fall in the next range. The program averages 10 readings "
     "per measurement to reduce noise.")

# ---------------- 4 ----------------
doc.add_heading("4. Circuit and wiring", level=1)
para("The sensor takes power from the Arduino's 5V and GND pins and sends its signal to analog input A0. Each LED is driven by its "
     "own digital pin through a 220 Ω series resistor, with all cathodes returning to GND. The 9 V battery feeds VIN through switch S1.")
figure(REPO + "/diagrams/circuit_diagram.png", "Figure 2 – Circuit diagram", 16.5)
table([["From", "To"],
       ["LM35 pin 1 (+Vs)", "Arduino 5V"],
       ["LM35 pin 2 (Vout)", "Arduino A0"],
       ["LM35 pin 3 (GND)", "Arduino GND"],
       ["Arduino D8", "220 Ω → blue LED anode (long leg)"],
       ["Arduino D9", "220 Ω → orange LED anode (long leg)"],
       ["Arduino D10", "220 Ω → red LED anode (long leg)"],
       ["All LED cathodes (short leg)", "Arduino GND"],
       ["9 V battery + (red lead)", "Switch S1 → Arduino VIN"],
       ["9 V battery − (black lead)", "Arduino GND"]], [7, 9.6])
para("LM35 pins are numbered 1 to 3 from left to right, with the flat face toward you and the legs pointing down.")
doc.add_heading("Resistor calculation", level=2)
para("A digital pin outputs 5 V and a coloured LED drops about 2 V. For a current of about 14 mA:")
equation("R = (Vcc − V_LED) / I_LED = (5 V − 2 V) / 14 mA ≈ 214 Ω → 220 Ω (standard value)")
para("This keeps each LED well under its 20 mA rating and within the Arduino pin limit.")
doc.add_heading("Battery power", level=2)
para("The detector runs from a 9 V battery connected to the Arduino's VIN pin through an on/off switch. The on-board regulator turns "
     "the 9 V into a steady 5 V for the LM35 and the LEDs, so the code and the temperature formula do not change.")
bullets([("VIN, not 5V: ", "VIN goes through the regulator, which accepts 7–12 V. Connecting 9 V to the 5V pin would damage the board."),
         ("Simpler option: ", "a 9 V battery clip with a 2.1 mm barrel plug fits the Arduino's power jack and feeds the same regulator; unplug it to switch off."),
         ("Battery life: ", "the circuit draws about 50–60 mA (board plus one LED), so a 9 V alkaline battery of about 500 mAh lasts roughly 8 hours."),
         ("Weak battery: ", "below about 7 V the regulator can no longer hold 5 V and the readings drift, so replace the battery if values look wrong."),
         ("USB and battery together ", "are safe while uploading: the board switches to the higher supply automatically.")])

# ---------------- 5 ----------------
doc.add_heading("5. Algorithm", level=1)
para("The program is an endless loop with two decisions. The limits are checked in order, 20 °C first and then 40 °C, so every "
     "temperature falls into exactly one branch.")
figure(REPO + "/diagrams/flowchart.png", "Figure 3 – Flowchart", 11)
bullets(["Set D8, D9 and D10 as outputs and turn all LEDs off; start the serial port at 9600 baud.",
         "Read A0 ten times and average the readings.",
         "Convert the average to °C with T = raw × 500 / 1024.",
         "If T ≤ 20, turn on blue; else if T ≤ 40, turn on orange; else turn on red. The other two LEDs are turned off.",
         "Print T and the chosen colour to the Serial Monitor.",
         "Wait 500 ms and repeat from step 2."], style="List Number")

# ---------------- 6 ----------------
doc.add_heading("6. Code", level=1)
para("The program is split into two files in one sketch folder. temperature_logic.h holds the limits, the decision and the ADC "
     "conversion; it uses no Arduino functions, so it can also be tested on a PC. temperature_detector.ino reads the sensor and drives the LEDs.")
doc.add_heading("temperature_logic.h", level=2)
code(open(REPO + "/code/temperature_detector/temperature_logic.h").read())
doc.add_heading("temperature_detector.ino", level=2)
code(open(REPO + "/code/temperature_detector/temperature_detector.ino").read())
para("To upload: open the .ino file in the Arduino IDE, select Tools → Board → Arduino UNO and the correct port, then click Upload. "
     "Open the Serial Monitor at 9600 baud to see lines such as “Temperature: 24.4 C -> ORANGE (20 C < T <= 40 C)”.")
para("After uploading, unplug the USB cable, connect the 9 V battery and turn on the switch: the program starts by itself and keeps "
     "running from the battery.")

# ---------------- 7 ----------------
doc.add_heading("7. Testing and results", level=1)
para("The decision logic passed all 9 boundary tests on a PC; the hardware results below are to be filled in from the lab session.")
doc.add_heading("Logic test (PC)", level=2)
para("temperature_logic.h was compiled with g++ together with a small test program that feeds fixed temperatures to chooseLed().")
table([["Input T", "Expected LED", "Result"],
       ["−10.0 °C", "Blue", "Pass"], ["0.0 °C", "Blue", "Pass"], ["19.9 °C", "Blue", "Pass"],
       ["20.0 °C", "Blue", "Pass"], ["20.1 °C", "Orange", "Pass"], ["30.0 °C", "Orange", "Pass"],
       ["40.0 °C", "Orange", "Pass"], ["40.1 °C", "Red", "Pass"], ["100.0 °C", "Red", "Pass"]], [5, 6, 5])
para("The full sketch was also compiled against stand-in Arduino functions: with raw values 30, 42 and 83 exactly one LED was HIGH "
     "each time (blue, orange, red).")
doc.add_heading("Hardware test", level=2)
table([["Condition", "Expected LED", "Serial Monitor reading", "Observed LED"],
       ["Room air", "Orange", "[__ °C]", "[fill in]"],
       ["Ice pack in a plastic bag on the sensor", "Blue", "[__ °C]", "[fill in]"],
       ["Warm air from a hair dryer, held at a distance", "Red", "[__ °C]", "[fill in]"]], [6.6, 3, 4, 3])

# ---------------- 8 ----------------
doc.add_heading("8. Discussion and conclusion", level=1)
para("The detector meets the specification: it converts the LM35 voltage to °C, applies the two limits with the required "
     "boundaries, and keeps exactly one LED on.")
para("Limitations observed in the design:")
bullets([("Resolution: ", "one ADC step is about 0.49 °C, so readings move in half-degree steps."),
         ("Flicker at a limit: ", "when T sits right at 20 or 40 °C, noise can make two LEDs alternate. Averaging 10 samples reduces this but does not remove it."),
         ("Reference voltage: ", "the conversion assumes exactly 5 V; a weak battery shifts the reading.")])
para("Possible improvements:")
bullets(["Add hysteresis, for example switch to orange above 20.5 °C and back to blue below 19.5 °C.",
         "Use the 1.1 V internal reference (analogReference(INTERNAL)) for about 0.1 °C resolution, since the LM35 output stays under 1.1 V up to 110 °C.",
         "Add an LCD to show the value without a PC, and a buzzer alarm above 40 °C."], style="List Number")
para("In conclusion, the project shows a complete sense–compare–act control loop on a microcontroller, from the sensor maths to the "
     "wiring, battery power and the tested decision logic.")

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print("saved", OUT)
