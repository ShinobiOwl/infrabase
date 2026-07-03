from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>InfraBase</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #0f172a; color: #e2e8f0; }
            .container { max-width: 600px; margin: 0 auto; text-align: center; padding: 40px; }
            h1 { color: #38bdf8; }
            .status { background: #1e293b; padding: 20px; border-radius: 8px; margin: 20px 0; }
            .badge { display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 14px; }
            .badge-green { background: #22c55e; color: #fff; }
            .version { color: #94a3b8; font-size: 14px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 InfraBase</h1>
            <div class="status">
                <p><span class="badge badge-green">● LIVE</span></p>
                <p>CI/CD Pipeline — Jenkins + Docker + OCIR</p>
                <p>Deployed via automated pipeline</p>
            </div>
            <div class="version">v1.0.0</div>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)