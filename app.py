import re
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def parse_quiz_file(filename="tailieu.txt"):
    """
    Hàm này đọc và phân tích file văn bản chứa câu hỏi trắc nghiệm.
    Nó trả về một danh sách các đối tượng câu hỏi theo định dạng mà
    file index.html yêu cầu.
    """
    questions = []
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Tách file thành các khối câu hỏi dựa trên "Câu X."
    question_blocks = re.split(r'\nCâu \d+\.', '\n' + content)
    
    # Bỏ qua phần tử rỗng đầu tiên
    if not question_blocks[0].strip():
        question_blocks = question_blocks[1:]

    for i, block in enumerate(question_blocks, 1):
        lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
        
        if not lines:
            continue
            
        # Dòng đầu tiên là nội dung câu hỏi
        question_text = lines[0]
        
        # Các dòng tiếp theo là lựa chọn và đáp án
        options_list = []
        correct_answer = ''
        
        for line in lines[1:]:
            if line.startswith('Đáp án:'):
                correct_answer = line.split(': ')[1].strip()
            # Kiểm tra xem dòng có phải là một lựa chọn không (A., B., C., D.)
            elif re.match(r'^[A-D]\.', line):
                letter = line[0]
                # Lấy text sau ký tự '.' và khoảng trắng
                text = line[3:]
                options_list.append({
                    "letter": letter,
                    "text": text
                })
        
        if question_text and len(options_list) > 0 and correct_answer:
            questions.append({
                "id": i,
                "question": question_text,
                "options": options_list,
                "answer": correct_answer
            })
            
    return questions

# Route chính để hiển thị trang web
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint để cung cấp dữ liệu câu hỏi cho frontend
@app.route('/api/questions')
def get_questions():
    # Phân tích file và trả về dữ liệu dạng JSON
    quiz_questions = parse_quiz_file()
    return jsonify(quiz_questions)

if __name__ == '__main__':
    app.run(debug=True)