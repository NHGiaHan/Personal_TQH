import streamlit as st
import pandas as pd
import plotly.express as px

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Phân tích AI Agent - CS", page_icon="🌸", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #FFF6F7; }
    h1, h2, h3 { color: #FF9AA2; font-family: 'Arial', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #FFDAC1; border-radius: 10px 10px 0px 0px; padding: 10px 20px; font-weight: bold; color: #555; }
    .stTabs [aria-selected="true"] { background-color: #FFB7B2; color: white;}
</style>
""", unsafe_allow_html=True)

st.title("🌸 Trực Quan Hóa & Đề Xuất Ứng Dụng AI Agent")
st.subheader("Trọng tâm: Ngành Khoa học Máy tính (Computer Science)")
st.markdown("**Github Repository:** [NHGiaHan/Personal_TQH](https://github.com/NHGiaHan/Personal_TQH)")
st.divider()

# --- XỬ LÝ 4 TẬP DỮ LIỆU ---
@st.cache_data
def load_and_prepare_data():
    df_desires = pd.read_csv("domain_worker_desires.csv")
    df_metadata = pd.read_csv("domain_worker_metadata.csv")
    df_expert = pd.read_csv("expert_rated_technological_capability.csv")
    df_task = pd.read_csv("task_statement_with_metadata.csv") # Thêm tập dữ liệu số 4

    cs_occs = [
        'Computer Network Support Specialists', 'Information Technology Project Managers',
        'Computer Systems Engineers/Architects', 'Computer and Information Systems Managers',
        'Computer Programmers', 'Computer User Support Specialists',
        'Software Quality Assurance Analysts and Testers', 'Database Administrators',
        'Information Security Analysts', 'Web Developers', 'Computer Systems Analysts'
    ]

    cs_desires = df_desires[df_desires['Occupation (O*NET-SOC Title)'].isin(cs_occs)]
    cs_metadata = df_metadata[df_metadata['Occupation (O*NET-SOC Title)'].isin(cs_occs)]
    cs_expert = df_expert[df_expert['Occupation (O*NET-SOC Title)'].isin(cs_occs)]
    cs_task = df_task[df_task['Occupation (O*NET-SOC Title)'].isin(cs_occs)].copy()

    return cs_desires, cs_metadata, cs_expert, cs_task

cs_desires, cs_metadata, cs_expert, cs_task = load_and_prepare_data()

# --- TẠO 3 TAB ---
tab1, tab2, tab3 = st.tabs(["📊 1. Hiện Trạng Sử Dụng", "🔍 2. Phân Tích Điểm Mới", "💡 3. Khuyến Nghị AI Agent"])

with tab1:
    st.markdown("### Tần suất sử dụng AI/LLM cho từng nhóm tác vụ")
    usage_cols = [c for c in cs_metadata.columns if 'LLM Usage' in c]
    usage_data = []
    for col in usage_cols:
        task_name = col.split(' - ')[1]
        freq = cs_metadata[col].value_counts(normalize=True) * 100
        regular_use = freq.get('Daily', 0) + freq.get('Weekly', 0)
        usage_data.append({'Tác vụ': task_name, 'Tỷ lệ dùng thường xuyên (%)': regular_use})

    df_usage = pd.DataFrame(usage_data).sort_values('Tỷ lệ dùng thường xuyên (%)', ascending=True)
    fig1 = px.bar(df_usage, x='Tỷ lệ dùng thường xuyên (%)', y='Tác vụ', orientation='h',
                  color='Tỷ lệ dùng thường xuyên (%)', color_continuous_scale='Mint',
                  title="Tỷ lệ nhân sự IT sử dụng AI thường xuyên (Daily/Weekly)")
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)
    st.info("**👉 Phân tích:** Nhân sự IT dùng AI chủ yếu để Tìm kiếm thông tin và Viết Code. Tuy nhiên, ở các tác vụ kiến trúc cấp cao như *Thiết kế hệ thống* hay *Ra quyết định*, tỷ lệ sử dụng lại cực thấp.")

# --- TRONG TAB 2: Phân tích nghịch lý chuyên gia ---
with tab2:
    st.markdown("### 🔍 Phân tích chuyên sâu: Nghịch lý chuyên gia")
    # Biểu đồ Scatter: Chuyên môn vs Tần suất dùng AI
    fig_paradox = px.scatter(cs_metadata, x='Experience', y='LLM Usage by Type - Coding', 
                             color='Education', size='Age',
                             title="Sự tương quan: Kinh nghiệm làm việc vs Mức độ tin tưởng dùng AI viết Code")
    st.plotly_chart(fig_paradox, use_container_width=True)
    
    st.markdown("""
    **Phát hiện mới:** Dữ liệu cho thấy ở nhóm chuyên gia có 6-10 năm kinh nghiệm, xu hướng sử dụng AI để "viết code trực tiếp" thấp hơn hẳn nhóm mới vào nghề. 
    **Kết luận:** Chuyên gia không dùng AI để làm thay, họ dùng AI để làm "trợ lý phân tích rủi ro".
    """)

# --- TRONG TAB 3: Kiến trúc Multi-Agent phân tầng ---
with tab3:
    st.markdown("### 💡 Khuyến nghị: Kiến trúc AI theo trình độ (Skill-based AI)")
    
    # Vẽ biểu đồ ngang phân loại tác vụ theo độ khó
    st.write("Cấu trúc AI Agent được đề xuất dựa trên phân tích dữ liệu:")
    data_rec = pd.DataFrame({
        'Cấp độ người dùng': ['Novice', 'Intermediate', 'Expert'],
        'Vai trò AI': ['Giảng viên (Mentor)', 'Lập trình viên (Coder)', 'Kiểm định viên (Auditor)'],
        'Trọng tâm AI': ['Kiến thức cơ bản', 'Tối ưu hiệu suất', 'Quét lỗi & Bảo mật']
    })
    st.table(data_rec)
    
    st.success("""
    **Chiến lược triển khai:** Thay vì ép AI làm mọi thứ, doanh nghiệp nên phân quyền AI Agent theo từng tầng kiến thức. 
    Điều này giúp giải quyết tận gốc rào cản 'Niềm tin' và 'Chất lượng' mà chúng ta đã phát hiện ở Tab 2.
    """)
