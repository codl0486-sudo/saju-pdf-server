from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import io
import base64
import os

app = Flask(__name__)
CORS(app)  # 모든 도메인에서 접근 허용

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "service": "사주 PDF 생성 서버",
        "endpoints": {
            "/generate-pdf": "POST - HTML을 PDF로 변환"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.json
        
        if not data or 'html' not in data:
            return jsonify({"error": "HTML 내용이 필요합니다"}), 400
        
        html_content = data['html']
        filename = data.get('filename', 'saju_report.pdf')
        
        # 기본 CSS (A4, 한글 폰트)
        base_css = CSS(string='''
            @page {
                size: A4;
                margin: 0;
            }
            
            @font-face {
                font-family: 'Noto Serif KR';
                src: url('https://fonts.gstatic.com/s/notoserifkr/v20/3JnmSDn90Gmq2mr3blnHaTZXTihC8O1ZNH1ahck.woff2') format('woff2');
                font-weight: 400;
            }
            
            @font-face {
                font-family: 'Noto Serif KR';
                src: url('https://fonts.gstatic.com/s/notoserifkr/v20/3JnmSDn90Gmq2mr3blnHaTZXTihC8O1ZNH1ahck.woff2') format('woff2');
                font-weight: 700;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Noto Serif KR', 'Malgun Gothic', serif;
                font-size: 10pt;
                line-height: 1.7;
                color: #333;
            }
        ''')
        
        font_config = FontConfiguration()
        
        # HTML을 PDF로 변환
        html = HTML(string=html_content)
        pdf_buffer = io.BytesIO()
        html.write_pdf(pdf_buffer, stylesheets=[base_css], font_config=font_config)
        pdf_buffer.seek(0)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-pdf-base64', methods=['POST'])
def generate_pdf_base64():
    """PDF를 Base64로 반환 (브라우저에서 바로 열기용)"""
    try:
        data = request.json
        
        if not data or 'html' not in data:
            return jsonify({"error": "HTML 내용이 필요합니다"}), 400
        
        html_content = data['html']
        
        base_css = CSS(string='''
            @page { size: A4; margin: 0; }
            body { font-family: 'Noto Serif KR', 'Malgun Gothic', serif; }
        ''')
        
        font_config = FontConfiguration()
        html = HTML(string=html_content)
        pdf_bytes = html.write_pdf(stylesheets=[base_css], font_config=font_config)
        
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        return jsonify({
            "success": True,
            "pdf_base64": pdf_base64
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
