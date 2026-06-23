import streamlit as st
import pandas as pd
import plotly.express as px

# --- CẤU HÌNH GIAO DIỆN PASTEL ---
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

# --- TIỀN XỬ LÝ DỮ LIỆU ---
@st.cache_data
def load_and_prepare_data():
    df_desires = pd.read_csv("domain_worker_desires.csv")
    df_metadata = pd.read_csv("domain_worker_metadata.csv")
    df_expert = pd.read_csv("expert_rated_technological_capability.csv")
    
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
    
    return cs_desires, cs_metadata, cs_expert

cs_desires, cs_metadata, cs_expert = load_and_prepare_data()

# --- TẠO 3 TAB CHO LUỒNG LOGIC PHÂN TÍCH ---
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

with tab2:
    st.markdown("### Nghịch lý tự động hóa & Nhu cầu kiểm soát")
    col1, col2 = st.columns(2)
    
    with col1:
        avg_cap = cs_expert['Automation Capacity Rating'].mean()
        avg_des = cs_desires['Automation Desire Rating'].mean()
        avg_agency = cs_desires['Human Agency Scale Rating'].mean()
        
        df_gap = pd.DataFrame({
            'Chỉ số đánh giá': ['Năng lực của AI', 'Mong muốn tự động hóa', 'Nhu cầu con người kiểm soát'],
            'Điểm trung bình (1-5)': [avg_cap, avg_des, avg_agency]
        })
        
        fig2 = px.bar(df_gap, x='Chỉ số đánh giá', y='Điểm trung bình (1-5)', text_auto='.2f',
                      color='Chỉ số đánh giá', color_discrete_sequence=['#B5EAD7', '#FF9AA2', '#C7CEEA'])
        fig2.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        
    with col2:
        reason_cols = [c for c in cs_desires.columns if 'Reasons for Human Agency' in c]
        reason_counts = cs_desires[reason_cols].sum().reset_index()
        reason_counts.columns = ['Lý do', 'Số lượng người chọn']
        reason_counts['Lý do'] = reason_counts['Lý do'].apply(lambda x: x.split(' - ')[1])
        reason_counts = reason_counts.sort_values('Số lượng người chọn', ascending=True)
        
        fig3 = px.bar(reason_counts, x='Số lượng người chọn', y='Lý do', orientation='h',
                      color='Số lượng người chọn', color_continuous_scale='Purp')
        fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)

    st.success("**👉 Điểm mới phát hiện (Insight):** Dù AI có năng lực cao, dân IT vẫn giữ quyền kiểm soát. Rào cản lớn nhất không phải là Nỗi lo mất việc, mà là **Quality Oversight (Nhu cầu kiểm duyệt chống bug)** và **Domain Knowledge (Sự thiếu hụt kiến thức nghiệp vụ của AI)**.")

with tab3:
    st.markdown("### 💡 Khuyến nghị ý tưởng ứng dụng AI Agent")
    st.markdown("""
    <div style='background-color: white; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);'>
        <h4 style='color: #FFB7B2;'>1. Domain-Anchored AI Agents (AI Agent neo kiến thức nghiệp vụ)</h4>
        <p>Ứng dụng kỹ thuật RAG kết nối AI với cơ sở dữ liệu nội bộ (Github Repos, tài liệu Jira) để bù đắp điểm yếu <b>Domain Knowledge</b> trước khi Agent đề xuất cấu trúc hệ thống.</p>
        <h4 style='color: #FFB7B2;'>2. Glass-box Agent với cơ chế "Human-in-the-loop"</h4>
        <p>Để giải quyết nỗi lo về <b>Quality Oversight</b>, AI Agent phải xuất ra sơ đồ logic giải thích bước đi của mình trước khi sinh code. Luôn cần một bước Lập trình viên nhấn <b>Approve/Reject</b> để duyệt.</p>
    </div>
    """, unsafe_allow_html=True)
