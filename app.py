#toàn bộ nội dung của cell này vào một file tên là app.py
import streamlit as st
import pandas as pd
import plotly.express as px  #thư viện của plotpy cho phép di chuột để xem biểu đồ, phóng to, thu nhỏ

# --- 1. CẤU HÌNH GIAO DIỆN PASTEL ---
st.set_page_config(page_title="Phân tích AI Agent - CS", page_icon="🌸", layout="wide")  #đặt tiêu đề tab trình duyệt

#chèn CSS thuần vào trang để đổi màu sắc
st.markdown("""
<style>
    .stApp { background-color: #FFF6F7; }  
    h1, h2, h3 { color: #FF9AA2; font-family: 'Arial', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #FFDAC1; border-radius: 10px 10px 0px 0px; padding: 10px 20px; font-weight: bold; color: #555; }
    .stTabs [aria-selected="true"] { background-color: #FFB7B2; color: white;}
    .css-1v0mbdj.etr89bj1 { border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

#in 
st.title("🌸 Báo cáo Phân Tích & Đề Xuất Ứng Dụng AI Agent")
st.subheader("Trọng tâm: Ngành Khoa học Máy tính (Computer Science)")
st.markdown("**Github Repository:** [NHGiaHan/Personal_TQH](https://github.com/NHGiaHan/Personal_TQH) | **Phương pháp:** Hệ thống hóa dữ liệu 5 bước")  #tạo hyperlink code nguồn (lưu ở github)
st.divider()   #đường kẻ ngang phân cách phần  trên và dưới 

# --- 2. TIỀN XỬ LÝ 4 TẬP DỮ LIỆU ---
#hàm @st.cache_data: hàm này tốn thời gian (đọc file CSV), nên lần đầu chạy xong thì lưu kq lại, lần sau tự lấy kq khôg cần đọc lại
@st.cache_data
def load_and_prepare_data():
    df_desires = pd.read_csv("domain_worker_desires.csv")
    df_metadata = pd.read_csv("domain_worker_metadata.csv")
    df_expert = pd.read_csv("expert_rated_technological_capability.csv")
    df_task = pd.read_csv("task_statement_with_metadata.csv")

    cs_occs = [
        'Computer Network Support Specialists', 'Information Technology Project Managers',
        'Computer Systems Engineers/Architects', 'Computer and Information Systems Managers',
        'Computer Programmers', 'Computer User Support Specialists',
        'Software Quality Assurance Analysts and Testers', 'Database Administrators',
        'Information Security Analysts', 'Web Developers', 'Computer Systems Analysts'
    ]

#lọc dl, chỉ giữ lại dòng có giá trị cột trog mảng cs_occs
    cs_desires = df_desires[df_desires['Occupation (O*NET-SOC Title)'].isin(cs_occs)]
    cs_metadata = df_metadata[df_metadata['Occupation (O*NET-SOC Title)'].isin(cs_occs)].copy()
    cs_expert = df_expert[df_expert['Occupation (O*NET-SOC Title)'].isin(cs_occs)]
    cs_task = df_task[df_task['Occupation (O*NET-SOC Title)'].isin(cs_occs)].copy()

    return cs_desires, cs_metadata, cs_expert, cs_task

cs_desires, cs_metadata, cs_expert, cs_task = load_and_prepare_data()

# --- 3. XÂY DỰNG TABS GIAO DIỆN ---
tab1, tab2, tab3 = st.tabs(["📊 Tổng Quan Hiện Trạng", "🔍 Phân Tích Chuyên Sâu (Deep Dive)", "💡 Khuyến Nghị Giải Pháp"])

# ==========================================
# TAB 1: HIỆN TRẠNG (MỤC 1): TẦN SUẤT SỬ DỤNG THEO PHAN LOẠI TÁC VỤ (TỔNG QUAN & RIÊNG TỪNG TÁC VỤ)
# ==========================================
with tab1:
    st.markdown("### Mục 1: Tần suất ứng dụng LLM theo phân loại tác vụ kỹ thuật")  #này là cho định dạng, ### là định dạng kích cỡ tiêu đề (#, ##,###...s)
    occ_options = ["🌟 Tất cả các vị trí (All CS Occupations)"] + list(cs_metadata['Occupation (O*NET-SOC Title)'].unique())  #unique đảm bảo hiển thị khôg trùng nhau
    selected_occ = st.selectbox("🎯 Bộ lọc phân khúc chức danh:", occ_options)   #tạo một dropdown menu cho người dùng chọn

    if selected_occ == "🌟 Tất cả các vị trí (All CS Occupations)":
        filtered_df = cs_metadata
        title_chart = "Tỷ lệ nhân sự kỹ thuật ứng dụng AI thường xuyên (Tổng quan ngành)"
    else:
        filtered_df = cs_metadata[cs_metadata['Occupation (O*NET-SOC Title)'] == selected_occ]
        title_chart = f"Tỷ lệ ứng dụng AI thường xuyên của: {selected_occ}"

    st.caption(f"**📌 Cỡ mẫu phân tích (Sample Size):** Dữ liệu được tính toán dựa trên **{len(filtered_df)}** nhân sự thuộc phân khúc này.")

    usage_cols = [c for c in filtered_df.columns if 'LLM Usage' in c]     #tạo list lấy tất cả tên cột nào có chứa chữ 'LLM Usage'
    usage_data = []
    for col in usage_cols:
        task_name = col.split(' - ')[1]    #tách tên cột tại dấu - và lấy phần phía sau dấu -
        freq = filtered_df[col].value_counts(normalize=True) * 100   # đếm số lần của mỗi cái (daily, weekly...) xuất hiện, normalize = true thì chia tỉ lệ %
        regular_use = freq.get('Daily', 0) + freq.get('Weekly', 0)   #lấy giá trị với key là daily và weekly, nếu nào khôg có thì =0, rồi + lại
        usage_data.append({'Tác vụ': task_name, 'Tỷ lệ dùng thường xuyên (%)': regular_use})     #Sau vòng lặp, usage_data sẽ là 1 list các dictionary, mỗi dictionary tương ứng 1 tác vụ, append là thêm 1 phần tử.

    df_usage = pd.DataFrame(usage_data).sort_values('Tỷ lệ dùng thường xuyên (%)', ascending=True)   #chuyển list các dictionary thành 1 bảng (DataFrame) có 2 cột
    
#Vẽ biểu đồ cột
    fig1 = px.bar(df_usage, x='Tỷ lệ dùng thường xuyên (%)', y='Tác vụ', orientation='h',   #orientation: cột ngang
                  color='Tỷ lệ dùng thường xuyên (%)', color_continuous_scale='Mint',
                  title=title_chart)
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')   #(màu nền) làm trong suốt khu vực vẽ biểu đô fva chứa biểu đồ
    st.plotly_chart(fig1, use_container_width=True)     #hiển thị biểu đồ lên web, giãn full chiều ngang khung chứa.

#hiện hướng dẫn, phần chữ phân tích, ** là in đậm chữ
    st.info("**👉 Data Storytelling:** Việc phân tích theo từng phân khúc chỉ ra rằng AI vẫn đang bị 'mắc kẹt' ở vai trò thợ gõ code/truy xuất thông tin. Nhóm kĩ sư chưa sẵn sàng tin tưởng giao phó các quyết định kiến trúc cốt lõi (System Design).")

# ==========================================
# TAB 2: ĐÀO SÂU MÂU THUẪN (MỤC 2, 3, 4)
# ==========================================
with tab2:
    st.markdown("### Phân tích đa chiều: Giải mã sự đứt gãy niềm tin công nghệ")   #title

    # --- MỤC 2 ---
    st.subheader("Mục 2: Đối chiếu Năng lực tự động hóa thực tế với Nhu cầu kiểm soát (Human Agency)")
    col1, col2 = st.columns(2)   #chia khu vực hiển thị thành 2 cột 

    #tính giá trị trung bình cả cột
    with col1:
        avg_cap = cs_expert['Automation Capacity Rating'].mean()
        avg_des = cs_desires['Automation Desire Rating'].mean()
        avg_agency = cs_desires['Human Agency Scale Rating'].mean()

        #Tạo 1 bảng mới gồm 2 cột: tên chỉ số và điểm trung bình tương ứng (3 dòng = 3 chỉ số)
        df_gap = pd.DataFrame({
            'Chỉ số toán học': ['Năng lực tự động', 'Nguyện vọng tự động', 'Nhu cầu kiểm duyệt'],
            'Điểm trung bình (1-5)': [avg_cap, avg_des, avg_agency]
        })

        #bđồ cột, test_auto: tự động hiện số trên đầu mỗi cột, hiện 2 số sau phẩy: BIỂU ĐỒ KHẢ NĂNG/NGUYỆN VỌNG/NHU CẦU KIỂM DUYỆT
        fig2 = px.bar(df_gap, x='Chỉ số toán học', y='Điểm trung bình (1-5)', text_auto='.2f', color='Chỉ số toán học',
                      color_discrete_sequence=['#B5EAD7', '#FF9AA2', '#C7CEEA'])
        fig2.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

#Lọc ra các cột có chữ "Reasons for Human Agency" — đây thường là các cột dạng checkbox/0-1 (mỗi cột là 1 lý do, giá trị 1 nếu người đó chọn lý do này, 0 nếu không).
    with col2:
        reason_cols = [c for c in cs_desires.columns if 'Reasons for Human Agency' in c]
        reason_counts = cs_desires[reason_cols].sum().reset_index()        #chỉ lấy các cột đó ra thành 1 bảng con. tính tổng theo từng cột, sum trả về series có tên cột là index, biến index thành cột cho dễ ve bđồ
        reason_counts.columns = ['Lý do ràng buộc', 'Tần suất phản hồi']   #đổi tên 2 cột cho dễ đọc
        reason_counts['Lý do ràng buộc'] = reason_counts['Lý do ràng buộc'].apply(lambda x: x.split(' - ')[1])   #áp dụng 1 hàm cho từng giá trị trong cột đó., apply... : tách chuổi và lấy chuỗi sau -
        reason_counts = reason_counts.sort_values('Tần suất phản hồi', ascending=True)

#biểu đồ LÝ DO
        fig3 = px.bar(reason_counts, x='Tần suất phản hồi', y='Lý do ràng buộc', orientation='h',
                      color='Tần suất phản hồi', color_continuous_scale='Purp')
        fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)
    st.success("**👉 Insight Mục 2:** Rào cản lớn nhất là yêu cầu **Kiểm soát chất lượng loại bỏ Bug (Quality Oversight)** và sự thiếu hụt **Kiến thức miền đặc thù (Domain Knowledge)**.")

    st.divider()   #vẽ đường kẻ ngang 

    # --- MỤC 3: NGHỊCH LÝ CHUYÊN GIA & KIỂM CHỨNG GIẢ THUYẾT ĐỐI VỚI TYPE CODING ---
    st.subheader("Mục 3: Nghịch lý Chuyên gia (Expertise Paradox) trong Kỹ nghệ Phần mềm")

    # 3.1 Biểu đồ Hộp (Coding)
    mapping = {'Never': 1, 'Monthly': 2, 'Weekly': 3, 'Daily': 4}  #ánh xạ chữ thành số
    cs_metadata['Mức độ tin dùng AI Code'] = cs_metadata['LLM Usage by Type - Coding'].map(mapping)  #áp dụng ánh xạ trên toàn bộ
    exp_order = ['1-2 year', '3-5 years', '6-10 years', '11-15 years', '16-20 years', '21-30 years']  #hiển thị thứ tự kinh nghiệm theo mình muôn


    fig4 = px.box(cs_metadata, x='Experience', y='Mức độ tin dùng AI Code',
                  category_orders={'Experience': exp_order}, color='Experience',
                  title="3.1 Sự phân vị: Thâm niên kinh nghiệm thực tế vs Tần suất sử dụng AI sinh mã nguồn")
    fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

    # =========================================================
    # KIỂM CHỨNG TẤT CẢ TÁC VỤ (DROP-OFF RATE)
    # =========================================================
    st.markdown("#### 3.2 Kiểm chứng diện rộng: Độ sụt giảm niềm tin trên toàn bộ hệ thống tác vụ")

    # Phân loại 2 nhóm: Lính mới (< 5 năm) và Chuyên gia (> 6 năm)
    novice_mask = cs_metadata['Experience'].isin(['Less than 1 year', '1-2 year', '3-5 years'])
    senior_mask = cs_metadata['Experience'].isin(['6-10 years', '11-15 years', '16-20 years', '21-30 years', 'More than 10 years'])

    usage_cols_all = [c for c in cs_metadata.columns if 'LLM Usage' in c]
    dropoff_data = []

    for col in usage_cols_all:
        task_name = col.split(' - ')[1]

        # Tính % dùng thường xuyên cho Nhóm Lính mới
        novice_freq = cs_metadata[novice_mask][col].value_counts(normalize=True) * 100   #Lọc bảng chỉ giữ các dòng có novice_mask = True → chỉ còn dữ liệu của nhóm lính mới. với mỗi tác vụ tính riêng % cho lính mới
        novice_pct = novice_freq.get('Daily', 0) + novice_freq.get('Weekly', 0)

        # Tính % dùng thường xuyên cho Nhóm Chuyên gia
        senior_freq = cs_metadata[senior_mask][col].value_counts(normalize=True) * 100
        senior_pct = senior_freq.get('Daily', 0) + senior_freq.get('Weekly', 0)

        # sau các vòng lặp, dropoff_data sẽ là 1 list gồm 4 dictionary (4 dòng), vd: tac vụ coding, phân khuc lính mới, tỷ lệ; tác vụ coding, phân khúc chuyên gia, tỷ lệ.
        dropoff_data.append({'Tác vụ': task_name, 'Phân khúc': 'Lính mới (Novice < 5 năm)', 'Tỷ lệ dùng (%)': novice_pct})
        dropoff_data.append({'Tác vụ': task_name, 'Phân khúc': 'Chuyên gia (Senior > 6 năm)', 'Tỷ lệ dùng (%)': senior_pct})

    df_dropoff = pd.DataFrame(dropoff_data)
    # Sắp xếp tác vụ theo thứ tự giảm dần để tạo hiệu ứng dốc
    df_dropoff_sorted = df_dropoff.sort_values(by='Tỷ lệ dùng (%)', ascending=False)

    #vẽ bđồ
    #barmode='group': với mỗi giá trị trên trục x (mỗi tác vụ), vẽ nhiều cột cạnh nhau (1 cột/nhóm), thay vì chồng lên nhau.
    #color='Phân khúc': tô màu cột theo nhóm (Lính mới/Chuyên gia) — Plotly tự nhận biết và tách thành 2 series màu khác nhau.
    fig_drop = px.bar(df_dropoff_sorted, x='Tác vụ', y='Tỷ lệ dùng (%)', color='Phân khúc', barmode='group',   
                      color_discrete_sequence=['#FF9AA2', '#B5EAD7'],
                      title="Đối chiếu Tỷ lệ sử dụng AI: Nhóm Novice vs Nhóm Senior")
    fig_drop.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_drop, use_container_width=True)

    #Hộp thông báo này mặc định có nền màu vàng nhạt đi kèm với biểu tượng dấu chấm than tam giác (⚠️)
    st.warning("**👉 Bằng chứng định lượng (Data Storytelling):** Biểu đồ cột nhóm này đã trả lời triệt để nghi vấn về các tác vụ khác. Ở các tác vụ đơn giản (bên trái), hai cột đứng khá sát nhau. Nhưng khi dịch chuyển sang các tác vụ lõi (System Design, Decision), khoảng cách (Gap) giữa hai cột bị nới rộng thảm hại. Điều này chứng minh định lý: **Độ phức tạp và Rủi ro của quy trình nghiệp vụ tỷ lệ thuận với sự tẩy chay AI của nhóm Chuyên gia!**")

    st.divider()

    # --- MỤC 4: Đào sâu kỹ năng thực tế --- BIỂU ĐỒ TREEMAP
    st.subheader("Mục 4: Bản đồ phân cấp độ phức tạp kỹ năng (Task Complexity Map) trong CS")
     
      #astype: ép cột về dạng chữ, dùng regex xóa kí tự \'...
    cs_task['Skill_Clean'] = cs_task['Skill (O*NET Work Activity)'].astype(str).str.replace(r"[\[\]\']", "", regex=True)
    skill_counts = cs_task['Skill_Clean'].value_counts().reset_index()       #trả về số đếm thô mỗi kỹ năng xuất hiện bao nhiêu lần.
    skill_counts.columns = ['Thuộc tính Kỹ năng cốt lõi', 'Trọng số xuất hiện']
    top_skills = skill_counts[skill_counts['Thuộc tính Kỹ năng cốt lõi'] != 'nan'].head(12)   #bỏ dùng gtri nan, chỉ lấy 12 dòng đầu tiên (vì đã sort theo số đếm giảm dần mặc định của value_counts()) → 12 kỹ năng phổ biến nhất

      #vẽ ; margin=dict(...): Cấu hình khoảng cách lề (padding) bốn phía của khung biểu đồ (top, left, right, bottom)
    fig5 = px.treemap(top_skills, path=['Thuộc tính Kỹ năng cốt lõi'], values='Trọng số xuất hiện',
                      color='Trọng số xuất hiện', color_continuous_scale='Sunset')
    fig5.update_layout(margin=dict(t=10, l=10, r=10, b=10), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig5, use_container_width=True)
    st.error("**👉 Insight Mục 4:** Khoa học máy tính là tập hợp đa kỹ năng phức tạp. Một mô hình tác tử đơn lẻ không thể giải quyết bài toán đa biến này.")

# ==========================================
# TAB 3: KHUYẾN NGHỊ (MỤC 5)
# ==========================================
with tab3:
    st.markdown("### Mục 5: Khuyến nghị Mô hình Hệ đa tác tử tự động hóa (Multi-Agent System)")
    #bảng
    df_rec = pd.DataFrame({
        'Kiến trúc Tác tử (Specialized Agent)': ['1. System Architecture & Knowledge', '2. Code Generation & Refactoring', '3. Automated Verification & Testing'],
        'Cơ chế vận hành': ['Dùng Vector DB/RAG kết nối mã nguồn', 'LLM finetuned sinh và tối ưu mã', 'Phân tích mã tĩnh và sinh Unit Test'],
        'Khắc phục điểm nghẽn': ['Giải quyết rào cản Kiến thức miền', 'Giải phóng lao động tác vụ lặp', 'Giải quyết rủi ro Bugs/Quality Oversight']
    })

    #hiển thị bảng dữ liệu
    st.table(df_rec)
    #hiển thị một hộp thông báo thành công
    st.success("**🚀 Kết luận:** Sự kết hợp giữa chuỗi tác tử đa tầng (Multi-Agent) và cổng duyệt của con người (Human-in-the-loop) là lời giải duy nhất cho bài toán quản trị chất lượng phần mềm!")
