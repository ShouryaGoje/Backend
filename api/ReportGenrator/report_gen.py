
# [
#     {
#         "u_id": 903099,
#         "p_name": "Kunal2",
#         "time_array": [
#             0.0,
#             0.51,
#             1.04,
#             1.56,
#             2.09,
#             2.62,
#             3.13,
#             3.37
#         ],
#         "volume_array": [
#             0.0,
#             0.0133,
#             0.3889,
#             0.3889,
#             0.3378,
#             0.3378,
#             0.1378,
#             0.1378
#         ],
#         "date": "2024-02-15",
#         "total_volume": 3.1
#     }
# ]

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from io import BytesIO
import matplotlib.pyplot as plt
from django.http import HttpResponse
from io import BytesIO
import matplotlib
matplotlib.use('agg')



def draw(data,i):
    plt.close('all')
    fig = plt.figure(figsize=(4, 3))
    plt.plot(data[i]['time_array'],data[i]['volume_array'])
    plt.ylabel('L/min')
    plt.xlabel('time')
    imgdata = BytesIO()
    fig.savefig(imgdata, format='svg')
    
    imgdata.seek(0)  # rewind the data
    drawing=svg2rlg(imgdata)
    
    return drawing


def generate_report(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    for i in range(len(data)):
        if i == 0:
            drawing = draw(data, i)

            c.drawString(40, 750, f"Report                                   Name: {data[0]['p_name']}")
            c.drawString(40, 670, f"Volume : {data[i]['total_volume']}")
            renderPDF.draw(drawing, c, 100, 400)
        elif i == 1:
            drawing = draw(data, i)

            c.drawString(40, 360, f"Volume : {data[i]['total_volume']}")
            renderPDF.draw(drawing, c, 100, 90)
            c.showPage()
        else:
            if i % 2 == 0:
                drawing = draw(data, i)
                c.drawString(40, 750, f"Volume : {data[i]['total_volume']}")
                renderPDF.draw(drawing, c, 100, 480)
            else:
                drawing = draw(data, i)
                c.drawString(40, 440, f"Volume : {data[i]['total_volume']}")
                renderPDF.draw(drawing, c, 100, 170)
                c.showPage()

    c.save()

    # Create a response with the PDF content
    pdf_data = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response.write(pdf_data)

    return response





# if __name__ == "__main__":
 


    # fig = plt.figure(figsize=(4, 3))
    # plt.plot([1,2,3,4])
    # plt.ylabel('some numbers')

    # imgdata = BytesIO()
    # fig.savefig(imgdata, format='svg')
    # imgdata.seek(0)  # rewind the data

    # drawing=svg2rlg(imgdata)

    # c = canvas.Canvas('test2.pdf', pagesize=letter)
    # c.drawString(40, 750, "So nice it works")
    # c.drawString(40, 670, "So nice it works")
    # renderPDF.draw(drawing,c, 100, 400)
    # c.drawString(40, 360, "So nice it works")
    # renderPDF.draw(drawing,c, 100, 90)
    
    

    # c.showPage() 

    # c.drawString(40, 750, "So nice it works")
    # renderPDF.draw(drawing,c, 100, 480)
    # c.drawString(40, 440, "So nice it works")
    # renderPDF.draw(drawing,c, 100, 170)
    

    
    #  # Move to the next page
    # c.save()
