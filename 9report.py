from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4

width, height = letter

def draw(c , x , y , s):
    c.drawString(x*width , y*height , s)

def createPDF(name , age , sepsis , heartRate , bp , wbc):
    c = canvas.Canvas("Report.pdf")
    width, height = letter
    header = "-"*200
    c.drawString(0.0*width,0.95*height,header)
    c.drawString(0.1*width,0.9*height,"Name:")
    c.drawString(0.2*width,0.9*height, name)
    c.drawString(0.1*width,0.85*height,"Age:")
    c.drawString(0.2*width,0.85*height, age)
    c.drawString(0,0.8*height,header)
    c.drawString(0.1*width , 0.75*height , "Heart Rate")
    draw(c , 0.8 , 0.75 , heartRate)
    c.drawString(0.1*width , 0.7*height , "Blood Pressure")
    draw(c , 0.8 , 0.7, bp)
    c.drawString(0.1*width , 0.65*height , "WBC count")
    draw(c , 0.8 , 0.65 , wbc)
    #Cheange values
    c.drawString(0.1*width , 0.45*height , "Condition")
    draw(c , 0.12 , 0.4 , "Sepsis: ")
    draw(c , 0.8 , 0.45 , "Status")
    
    draw(c , 0.8 , 0.40 , sepsis)
    draw(c , 0.78 , 0.38 , "(>0.2 // Positive)")
    draw(c , 0.78 , 0.36 , "(<0.2 // Negative)")
    c.drawString(0.1*width , 0.3*height , "Remarks")
    c.drawString(0.1*width , 0.28*height , "The patient has sepsis. Suggested to admit in hospital as soon as possible.")
    c.showPage()
    c.save()
    # c.drawString(0.1*width,0.9*height,"Hello World")
    # c.drawString(0.1*width,0.89*height,"Hello World")

createPDF("Aditya" , "19" , "Positive" , "37" , "120/24" , "1")