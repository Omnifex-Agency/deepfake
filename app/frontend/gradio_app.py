"""
DeepShield AI — Standalone Gradio 5 Forensic Demonstration App
Provides interactive visual, acoustic, and multimodal media forensic evaluation tabs.
"""

import os
import io
import cv2
import numpy as np
from PIL import Image
import gradio as gr

from app.engine.multimodal_engine import MultimodalEngine

# Initialize forensic engine
print("[Gradio App] Loading DeepShield Multimodal Engine...")
engine = MultimodalEngine(
    image_ckpt="experiments/image/checkpoints/deepshield_best.pt",
    audio_ckpt="experiments/audio/checkpoints/whisper_specrnet_best.pt",
    fusion_ckpt="experiments/multimodal/checkpoints/deepshield_fusion.pt",
    device="cpu",
)
print("[Gradio App] Engine ready!")


def predict_image(image_input):
    if image_input is None:
        return "No image provided.", None, None, {}

    if isinstance(image_input, np.ndarray):
        pil_img = Image.fromarray(image_input)
    else:
        pil_img = image_input

    report = engine.analyze_image(pil_img)
    img_res = report["image_forensics"]

    verdict_text = f"### Verdict: {report['overall_risk_label']}\n**Calibrated Risk Probability:** {img_res['calibrated_probability']:.2%}\n**95% Confidence Interval:** [{img_res['confidence_interval_95']['lower']:.3f}, {img_res['confidence_interval_95']['upper']:.3f}]\n\n{report['verdict']}"

    # Decode overlay image
    b64_overlay = img_res["artifacts"]["overlay_b64"]
    b64_clean = b64_overlay.split(",")[1]
    import base64
    overlay_bytes = base64.b64decode(b64_clean)
    overlay_pil = Image.open(io.BytesIO(overlay_bytes))

    telemetry = {
        "Calibrated Probability": img_res["calibrated_probability"],
        "Raw Probability": img_res["raw_probability"],
        "Calibration Temperature": img_res["calibration_temperature"],
        "Peak Anomaly Hotspot (X, Y)": f"({img_res['peak_anomaly_coordinate']['x']}, {img_res['peak_anomaly_coordinate']['y']})",
        "Modality Fallback": "Active (Audio Absent)",
    }

    return verdict_text, overlay_pil, telemetry


def predict_audio(audio_path):
    if audio_path is None:
        return "No audio provided.", None, {}

    report = engine.analyze_audio(audio_path)
    aud_res = report["audio_forensics"]

    verdict_text = f"### Verdict: {report['overall_risk_label']}\n**Calibrated Risk Probability:** {aud_res['calibrated_probability']:.2%}\n**95% Confidence Interval:** [{aud_res['confidence_interval_95']['lower']:.3f}, {aud_res['confidence_interval_95']['upper']:.3f}]\n\n{report['verdict']}"

    import base64
    b64_anomaly = aud_res["artifacts"]["anomaly_spectrogram_b64"].split(",")[1]
    anomaly_bytes = base64.b64decode(b64_anomaly)
    anomaly_pil = Image.open(io.BytesIO(anomaly_bytes))

    telemetry = {
        "Calibrated Risk Probability": aud_res["calibrated_probability"],
        "Calibration Temperature": aud_res["calibration_temperature"],
        "Duration (Seconds)": aud_res["audio_duration_seconds"],
        "Vocal Fundamental Ratio": aud_res["spectral_bands"]["vocal_fundamental_ratio"],
        "Vocoder Highband Ratio": aud_res["spectral_bands"]["vocoder_highband_ratio"],
    }

    return verdict_text, anomaly_pil, telemetry


# Build Gradio UI
with gr.Blocks(title="DeepShield AI — Forensic Media Detection", theme=gr.themes.Soft(primary_hue="cyan")) as demo:
    gr.Markdown("# 🛡️ DeepShield AI — Multimodal Deepfake Media Detection System")
    gr.Markdown("Research-grade explainable forensic analysis across image, audio, and multimodal video media.")

    with gr.Tab("🖼️ Image Forensics (Grad-CAM Saliency)"):
        with gr.Row():
            with gr.Column():
                img_in = gr.Image(type="pil", label="Upload Facial Image")
                btn_img = gr.Button("Analyze Image", variant="primary")
            with gr.Column():
                verdict_out = gr.Markdown(label="Forensic Assessment")
                overlay_out = gr.Image(type="pil", label="Grad-CAM Anomaly Saliency Overlay")
                telemetry_out = gr.JSON(label="Forensic Telemetry")

        btn_img.click(predict_image, inputs=[img_in], outputs=[verdict_out, overlay_out, telemetry_out])

    with gr.Tab("🎙️ Audio Forensics (Spectral Harmonics)"):
        with gr.Row():
            with gr.Column():
                aud_in = gr.Audio(type="filepath", label="Upload Speech Audio (.wav)")
                btn_aud = gr.Button("Analyze Speech", variant="primary")
            with gr.Column():
                aud_verdict = gr.Markdown(label="Forensic Assessment")
                aud_spec = gr.Image(type="pil", label="Time-Frequency Anomaly Attribution")
                aud_telemetry = gr.JSON(label="Spectral Telemetry")

        btn_aud.click(predict_audio, inputs=[aud_in], outputs=[aud_verdict, aud_spec, aud_telemetry])

    gr.Markdown("---")
    gr.Markdown("*DeepShield AI Portfolio & Benchmark Artifact • Zero-Leakage Calibrated Models*")


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
