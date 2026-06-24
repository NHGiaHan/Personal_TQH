import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CẤU HÌNH GIAO DIỆN PASTEL ---
st.set_page_config(page_title="Phân tích AI Agent - CS", page_icon="🌸", layout="wide")
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

st.title("🌸 Báo cáo Phân Tích & Đề Xuất Ứng Dụng AI Agent")
st.subheader("Trọng tâm: Ngành Khoa học Máy tính (Computer Science)")
st.markdown("**Github Repository:** [NHGiaHan/Personal_TQH](https://github.com/NHGiaHan/Personal_TQH) | **Phương pháp:** Hệ thống hóa dữ liệu 5 bước")
st.divider()

# --- 2. TIỀN XỬ LÝ 4 TẬP DỮ LIỆU ---
@st.cache_data
def load_and_prepare_data():
    df_desires = pd.read_csv("domain_worker_desires.csv")
    df_metadata = pd.read_csv("domain_worker_metadata.csv")
    df_expert = pd.read_csv("expert_rated_technological_capability.csv")
    df_task = pd.read_csv("task_statement_with_metadata.csv")
    
    # Lọc chuyên ngành thuộc khối Computer Science & IT
    cs_occs = [
        'Computer Network Support Specialists',
        'Computer Systems Engineers/Architects',
        'Computer Programmers', 'Computer User Support Specialists',
        'Software Quality Assurance Analysts and Testers', 'Database Administrators',
        'Information Security Analysts', 'Web Developers', 'Computer Systems Analysts'
    ]
    
    cs_desires = df_desires[df_desires['Occupation (O*NET-SOC Title)'].isin(cs_occs)]
    cs_metadata = df_metadata[df_metadata['Occupation (O*NET-SOC Title)'].isin(cs_occs)].copy()
    cs_expert = df_expert[df_expert['Occupation (O*NET-SOC Title)'].isin(cs_occs)]
    cs_task = df_task[df_task['Occupation (O*NET-SOC Title)'].isin(cs_occs)].copy()
    
    return cs_desires, cs_metadata, cs_expert, cs_task

cs_desires, cs_metadata, cs_expert, cs_task = load_and_prepare_data()

# --- 3. XÂY DỰNG TABS GIAO DIỆN ---
tab1, tab2, tab3 = st.tabs(["📊 Tổng Quan Hiện Trạng", "🔍 Phân Tích Chuyên Sâu (Deep Dive)", "💡 Khuyến Nghị Giải Pháp"])

# ==========================================
# TAB 1: HIỆN TRẠNG (MỤC 1) - CÓ BỘ LỌC TƯƠNG TÁC
# ==========================================
with tab1:
    st.markdown("### Mục 1: Tần suất ứng dụng LLM theo phân loại tác vụ kỹ thuật")
    
    # --- BỘ LỌC PHÂN KHÚC (DATA SEGMENTATION) ---
    occ_options = ["🌟 Tất cả các vị trí (All CS Occupations)"] + list(cs_metadata['Occupation (O*NET-SOC Title)'].unique())
    selected_occ = st.selectbox("🎯 Bộ lọc phân khúc chức danh:", occ_options)
    
    # Xử lý logic lọc dữ liệu
    if selected_occ == "🌟 Tất cả các vị trí (All CS Occupations)":
        filtered_df = cs_metadata
        title_chart = "Tỷ lệ nhân sự kỹ thuật ứng dụng AI thường xuyên (Tổng quan ngành)"
    else:
        filtered_df = cs_metadata[cs_metadata['Occupation (O*NET-SOC Title)'] == selected_occ]
        title_chart = f"Tỷ lệ ứng dụng AI thường xuyên của: {selected_occ}"
    
    # Hiển thị cỡ mẫu để bảo vệ tính thống kê
    st.caption(f"**📌 Cỡ mẫu phân tích (Sample Size):** Dữ liệu được tính toán dựa trên **{len(filtered_df)}** nhân sự thuộc phân khúc này.")
    
    # Tính toán % dựa trên tập dữ liệu đã lọc (filtered_df)
    usage_cols = [c for c in filtered_df.columns if 'LLM Usage' in c]
    usage_data = []
    for col in usage_cols:
        task_name = col.split(' - ')[1]
        freq = filtered_df[col].value_counts(normalize=True) * 100
        regular_use = freq.get('Daily', 0) + freq.get('Weekly', 0)
        usage_data.append({'Tác vụ': task_name, 'Tỷ lệ dùng thường xuyên (%)': regular_use})
        
    df_usage = pd.DataFrame(usage_data).sort_values('Tỷ lệ dùng thường xuyên (%)', ascending=True)
    fig1 = px.bar(df_usage, x='Tỷ lệ dùng thường xuyên (%)', y='Tác vụ', orientation='h',
                  color='Tỷ lệ dùng thường xuyên (%)', color_continuous_scale='Mint',
                  title=title_chart)
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)
    
    st.info("**👉 Data Storytelling:** Việc phân tích theo từng phân khúc chỉ ra rằng, dù ở bất kỳ vị trí chuyên môn nào, AI vẫn đang bị 'mắc kẹt' ở vai trò thợ gõ code/truy xuất thông tin. Nhóm kĩ sư chưa sẵn sàng tin tưởng giao phó các quyết định kiến trúc cốt lõi (System Design) cho mô hình AI đơn lẻ.")

# ==========================================
# TAB 2: ĐÀO SÂU MÂU THUẪN (MỤC 2, 3, 4)
# ==========================================
with tab2:
    st.markdown("### Phân tích đa chiều: Giải mã sự đứt gãy niềm tin công nghệ")
    
    # --- MỤC 2: Nghịch lý kiểm soát ---
    st.subheader("Mục 2: Đối chiếu Năng lực tự động hóa thực tế với Nhu cầu kiểm soát (Human Agency)")
    col1, col2 = st.columns(2)
    with col1:
        avg_cap = cs_expert['Automation Capacity Rating'].mean()
        avg_des = cs_desires['Automation Desire Rating'].mean()
        avg_agency = cs_desires['Human Agency Scale Rating'].mean()
        df_gap = pd.DataFrame({
            'Chỉ số toán học': ['Năng lực tự động (Expert Rated)', 'Nguyện vọng tự động', 'Nhu cầu kiểm duyệt hệ thống'],
            'Điểm trung bình (1-5)': [avg_cap, avg_des, avg_agency]
        })
        fig2 = px.bar(df_gap, x='Chỉ số toán học', y='Điểm trung bình (1-5)', text_auto='.2f', color='Chỉ số toán học', 
                      color_discrete_sequence=['#B5EAD7', '#FF9AA2', '#C7CEEA'])
        fig2.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        
    with col2:
        reason_cols = [c for c in cs_desires.columns if 'Reasons for Human Agency' in c]
        reason_counts = cs_desires[reason_cols].sum().reset_index()
        reason_counts.columns = ['Lý do ràng buộc', 'Tần suất phản hồi']
        reason_counts['Lý do ràng buộc'] = reason_counts['Lý do ràng buộc'].apply(lambda x: x.split(' - ')[1])
        reason_counts = reason_counts.sort_values('Tần suất phản hồi', ascending=True)
        fig3 = px.bar(reason_counts, x='Tần suất phản hồi', y='Lý do ràng buộc', orientation='h', 
                      color='Tần suất phản hồi', color_continuous_scale='Purp')
        fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)
    st.success("**👉 Insight Mục 2:** Mặc dù năng lực kỹ thuật của AI được chuyên gia chấm rất cao (3.48), rào cản ứng dụng lớn nhất trong Khoa học máy tính là yêu cầu **Kiểm soát chất lượng loại bỏ Bug (Quality Oversight)** và sự thiếu hụt **Kiến thức miền đặc thù (Domain Knowledge)**.")

    st.divider()

    # --- MỤC 3: Nghịch lý chuyên gia ---
    st.subheader("Mục 3: Nghịch lý Chuyên gia (Expertise Paradox) trong Kỹ nghệ Phần mềm")
    mapping = {'Never': 1, 'Monthly': 2, 'Weekly': 3, 'Daily': 4}
    cs_metadata['Mức độ tin dùng AI Code'] = cs_metadata['LLM Usage by Type - Coding'].map(mapping)
    exp_order = ['1-2 year', '3-5 years', '6-10 years', '11-15 years', '16-20 years', '21-30 years']
    
    fig4 = px.box(cs_metadata, x='Experience', y='Mức độ tin dùng AI Code', 
                  category_orders={'Experience': exp_order}, color='Experience',
                  title="Sự phân vị: Thâm niên kinh nghiệm thực tế vs Tần suất sử dụng AI sinh mã nguồn")
    fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)
    st.warning("**👉 Insight Mục 3:** Biểu đồ hộp thể hiện độ phân tán lớn ở nhóm Senior (6-10 năm+). Các kỹ sư lão luyện cực kỳ thận trọng với AI vì họ thấu hiểu rủi ro hệ thống của các lỗi logic ẩn sâu, trái ngược với sự phụ thuộc của nhóm Novice.")

    st.divider()

    # --- MỤC 4: Đào sâu kỹ năng thực tế ---
    st.subheader("Mục 4: Bản đồ phân cấp độ phức tạp kỹ năng (Task Complexity Map) trong CS")
    cs_task['Skill_Clean'] = cs_task['Skill (O*NET Work Activity)'].astype(str).str.replace(r"[\[\]\']", "", regex=True)
    skill_counts = cs_task['Skill_Clean'].value_counts().reset_index()
    skill_counts.columns = ['Thuộc tính Kỹ năng cốt lõi', 'Trọng số xuất hiện']
    top_skills = skill_counts[skill_counts['Thuộc tính Kỹ năng cốt lõi'] != 'nan'].head(12)
    
    fig5 = px.treemap(top_skills, path=['Thuộc tính Kỹ năng cốt lõi'], values='Trọng số xuất hiện',
                      color='Trọng số xuất hiện', color_continuous_scale='Sunset')
    fig5.update_layout(margin=dict(t=10, l=10, r=10, b=10), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig5, use_container_width=True)
    st.error("**👉 Insight Mục 4:** Cấu trúc phân cấp Treemap chỉ ra Khoa học máy tính là một tập hợp đa kỹ năng đan xen từ Phân tích dữ liệu hệ thống đến Ra quyết định logic. Một mô hình tác tử đơn lẻ không thể giải quyết bài toán đa biến này.")

# ==========================================
# TAB 3: KHUYẾN NGHỊ (MỤC 5)
# ==========================================
with tab3:
    st.markdown("### Mục 5: Khuyến nghị Mô hình Hệ đa tác tử tự động hóa Kỹ nghệ phần mềm (Multi-Agent Software Engineering - MASE)")
    st.write("Tổng hợp từ chuỗi 4 bằng chứng định lượng phía trước, mô hình đề xuất cấu trúc giải pháp phân tầng các tác tử thông minh chuyên biệt (Specialized Agents) hoạt động theo kiến trúc luồng dữ liệu khép kín:")
    
    # Bảng cấu trúc định hướng Khoa học Máy tính
    df_rec = pd.DataFrame({
        'Kiến trúc Tác tử (Specialized Agent)': [
            '1. System Architecture & Knowledge Agent', 
            '2. Code Generation & Refactoring Agent', 
            '3. Automated Verification & Testing Agent'
        ],
        'Thuật toán & Cơ chế vận hành chính': [
            'Sử dụng Vector Database và RAG kết nối mã nguồn hệ thống để xử lý bài toán thiếu Domain Knowledge.',
            'Ứng dụng LLM finetuned chuyên biệt cho sinh mã, tối ưu hóa cấu trúc giải thuật và độ phức tạp tính toán.',
            'Áp dụng cơ chế Static Code Analysis (Phân tích mã tĩnh) và Formal Verification để tự động sinh Unit Test.'
        ],
        'Khắc phục điểm nghẽn thực tế (Từ đối chiếu dữ liệu)': [
            'Giải quyết triệt để rào cản thiếu hụt Kiến thức miền (Mục 2 & Mục 4).',
            'Giải phóng sức lao động ở các tác vụ thực thi lặp đi lặp lại có tần suất cao (Mục 1).',
            'Giải quyết khủng hoảng niềm tin về rủi ro Bugs và Quality Oversight của nhóm Chuyên gia (Mục 2 & Mục 3).'
        ],
        'Giao thức tương tác với Con người': [
            'Kỹ sư hệ thống kiểm duyệt bản thiết kế logic (System Blueprints).',
            'Lập trình viên rà soát cấu trúc mã nguồn.',
            'Senior Engineers / Tech Leads đóng vai trò kiểm duyệt tối cao (Human-in-the-loop) để nhấn nút Triển khai (Deploy).'
        ]
    })
    
    st.table(df_rec)
    
    st.success("""
    **🚀 Kết luận chiến lược (Actionable Recommendation):**
    
    Mô hình ứng dụng AI Agent tối ưu cho ngành Khoa học máy tính không phải là thay thế con người, mà là chuyển dịch vai trò của Kỹ sư máy tính từ **"Người trực tiếp sinh mã thủ công" (Manual Coder)** thành **"Người kiểm duyệt kiến trúc và logic thuật toán" (System Auditor)**. Sự kết hợp giữa chuỗi tác tử đa tầng (Multi-Agent) và cổng duyệt của con người (Human-in-the-loop) là lời giải duy nhất cho bài toán quản trị chất lượng phần mềm dựa trên dữ liệu thực tế!
    """)
