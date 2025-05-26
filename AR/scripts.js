let hat, leaf1, leaf2;
let handposeModel;
let specialEffectTriggered = false;  // 控制特效開關

// ✅ 確保 face-api.js 與 TensorFlow.js 版本正確
console.log(`✅ TensorFlow.js 版本: ${tf.version.tfjs}`);
console.log(`✅ face-api.js 版本: ${faceapi.version}`);

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        document.getElementById("video").srcObject = stream;
        console.log("✅ 攝影機已開啟");
    } catch (err) {
        console.error("❌ 無法開啟攝影機", err);
        alert("無法開啟攝影機，請檢查是否已授予權限！");
    }
}

// ✅ 確保模型正確載入
async function loadModels() {
    try {
        // 載入 Face-api.js 模型
        await faceapi.nets.tinyFaceDetector.loadFromUri('/models');
        await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
        await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
        console.log("✅ Face-api.js 模型載入完成！");

        // 載入 handpose 模型
        handposeModel = await handpose.load();
        console.log("✅ Handpose 模型載入完成！");

    } catch (err) {
        console.error("❌ 模型或資源載入錯誤", err);
        alert("模型或資源載入錯誤！請確認 /models/ 資料夾是否存在！");
    }
}

// ✅ 開始臉部偵測
async function detectFaces() {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    console.log("⌛ 開始臉部偵測...");
    setInterval(async () => {
        const detections = await faceapi.detectAllFaces(document.getElementById("video"), new faceapi.TinyFaceDetectorOptions());
        console.log(`🎯 偵測到 ${detections.length} 張臉`);

        ctx.clearRect(0, 0, canvas.width, canvas.height);  // 清空畫布

        detections.forEach(det => {
            const { x, y, width, height } = det.box;

            // 如果特效已觸發，則繪製
            if (specialEffectTriggered) {
                // 帽子
                const hatWidth = width;
                const hatHeight = hat.height * (hatWidth / hat.width);
                const hatX = x;
                const hatY = y - hatHeight * 0.3;
                ctx.drawImage(hat, hatX, hatY, hatWidth, hatHeight);

                // 葉子1
                const leaf1X = x - 50;
                let leaf1Y = y - 100;
                if (leaf1Y < 0) leaf1Y = 0;
                ctx.drawImage(leaf1, leaf1X, leaf1Y);

                // 葉子2
                const leaf2X = x + width - 50;
                let leaf2Y = y - 150;
                if (leaf2Y < 0) leaf2Y = 0;
                ctx.drawImage(leaf2, leaf2X, leaf2Y);
            }
        });
    }, 100);
}

// ✅ 偵測手勢
async function detectHands() {
    const predictions = await handposeModel.estimateHands(document.getElementById("video"));

    predictions.forEach(prediction => {
        const landmarks = prediction.landmarks;
        checkForYaGesture(landmarks); // 檢查 "比YA" 手勢
    });
}

// ✅ 檢查比YA手勢
function checkForYaGesture(landmarks) {
    const [thumb, index, middle, ring, pinky] = landmarks;

    // 假設比YA手勢是食指和大拇指的距離
    const thumbIndexDist = Math.abs(thumb[0] - index[0]);
    const indexMiddleDist = Math.abs(index[0] - middle[0]);

    if (thumbIndexDist > 30 && indexMiddleDist < 30) {
        console.log("🎉 偵測到比YA手勢！");
        if (!specialEffectTriggered) {
            specialEffectTriggered = true;  // 觸發特效
            console.log("✨ 特效已觸發！");
        }
    }
}

// ✅ 主程序
async function main() {
    try {
        // 設定 TensorFlow.js 使用 CPU 後端
        await tf.setBackend('cpu');
        console.log('✅ 已設定為 CPU 後端');
        
        // 開啟攝影機
        await startCamera();
        
        // 載入模型和圖片資源
        await loadModels();
        
        // 開始臉部偵測
        detectFaces();
        
        // 每 500ms 檢測一次手勢
        setInterval(detectHands, 500);
    } catch (error) {
        console.error('❌ 初始化錯誤', error);
    }
}

// ✅ 頁面載入時執行
window.onload = () => {
    if (typeof faceapi === "undefined") {
        console.error("❌ face-api.js 載入失敗！");
    } else {
        console.log("✅ face-api.js 載入成功");
        main();
    }
};
