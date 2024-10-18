import os
import streamlit as st
from reportlab.pdfgen import canvas
from annotated_text import annotated_text,annotation

from ShmooDataExtractorV1 import SHMViewer

# Streamlit app layout
st.set_page_config(page_title="Shmoo可视化",
                   page_icon='👀',layout="wide",
                   initial_sidebar_state="expanded")
st.header("SHMOO Visualization", divider='rainbow')

annotated_text(
        "This ",
        annotation("GUI","application","#8ef",font_family="Comic Sans MS"),
        " is for ",
        annotation("SHMOO","txt format","#fea",font_family="Comic Sans MS"),
        "  visualization of ",
        (" IG-XL CZ Tool","Teradyne services","#faa")
       )

# 左边栏设置
with st.sidebar:
    st.title("选择txt数据:")
    txt_list = st.file_uploader("Select CZ TXT file",
                                type="txt",
                                accept_multiple_files=True)

    st.title("输入文件夹路径，并且点击保存：")
    # 显示输入框接收文件夹路径
    folder_path = st.text_input(r'请输入文件夹路径:( e.g. __C:\Users\Go\Desktop__)')
    submit_btn = st.button(" __🖕Save to PDF__")

if txt_list:
    file_name =[]
    file_contents=[]

    for txt in txt_list:
        file_name.append(str(txt.name))
        file_contents.append(txt.read().decode("utf-8"))

    tabs = st.tabs(file_name)

    #读取Markdown文件内容并展示
    for i, file in enumerate(file_contents):
        with tabs[i]:
            P = SHMViewer(file)
            patterns = P.match_pattern()
            for pattern in patterns:
                headtxts = P.show_headfile(pattern).replace('   ','-').replace('\r\n', '  \n')
                #print(headtxts)
                st.info(headtxts)
                #st.info('**'+headtxts+'**')
                st.plotly_chart(P.plot_shm(pattern),use_container_width=True)
                #st.warning(P.show_tail(pattern))
                st.markdown('---')


    if submit_btn:
        # 检查是否输入了路径，并且该路径是否存在
        if folder_path is not None and os.path.exists(folder_path):
            try:
                for file_index, file in enumerate(file_contents):
                    pdf_file_name = folder_path + '/' + file_name[file_index].replace('.txt','.pdf')
                    # Create a new PDF file
                    pdf_file = canvas.Canvas(pdf_file_name,(1020,1000))
                    # 获取页面的宽度和高度
                    page_width, page_height = pdf_file._pagesize

                    P = SHMViewer(file)
                    patterns = P.match_pattern()
                    headtxtlist = []
                    pattern_index = 0
                    for pattern in patterns:
                        pattern_index += 1
                        headtxtlist = P.show_headfile(pattern).split('\r\n')
                        i=1
                        pdf_file.setFont(psfontname='Helvetica', size=20)
                        # psfontname='Helvetica'
                        for txt in headtxtlist[:-1]:
                            text_width, text_height = pdf_file.stringWidth(txt), pdf_file._leading
                            #pdf_file.drawString((page_width - text_width) / 2, page_height - i * text_height-100, txt)
                            pdf_file.drawString(30, page_height - i * text_height - 10, txt)
                            i+=1
                        # Convert the figure to an image
                        path = "tempShmdata/" + headtxtlist[0].replace('Test Suite Name = ','').replace(':','') + str(file_index)+'_'+ str(pattern_index) +'.png'
                        P.plot_shm(pattern).write_image(path,width=962, height=690)
                        pdf_file.drawImage(path, x=30, y=60,width=962, height=690)
                        pdf_file.showPage()
                    # Save the PDF file
                    pdf_file.save()

                    with st.sidebar:
                        st.success(file_name[file_index] + " is successfully!")
                st.balloons()

            except Exception as e:
                st.error(f"Error: {e}")
                with st.sidebar:
                    st.warning("Report Not Saved")
        else:
            with st.sidebar:
                st.error(f"路径不正确或者不存在！")







