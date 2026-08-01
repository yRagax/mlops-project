import os
import dotenv
import gradio as gr
import requests

# Load environmental variables
dotenv.load_dotenv()
DEMO_PORT = int(os.getenv("DEMO_PORT"))
API_PORT = int(os.getenv("API_PORT"))


def predict_house_value(
    api_url,
    longitude,
    latitude,
    housing_median_age,
    total_rooms,
    total_bedrooms,
    population,
    households,
    median_income,
):
    """
    Collects inputs, constructs JSON payload with exact feature names,
    and calls the model endpoint via POST request.
    """
    # Build payload using exact feature names requested
    payload = {
        "longitude": longitude.strip(),
        "latitude": latitude.strip(),
        "housing_median_age": housing_median_age.strip(),
        "total_rooms": total_rooms.strip(),
        "total_bedrooms": total_bedrooms.strip(),
        "population": population.strip(),
        "households": households.strip(),
        "median_income": median_income.strip(),
    }

    try:
        # Perform POST request to the API endpoint
        response = requests.post(api_url, json=payload, timeout=10)

        # Parse JSON response or fallback to raw text
        if response.status_code == 200:
            try:
                return response.json()
            except Exception:
                return {"error": response.text}
        else:
            return {"error": f"Error {response.status_code}: {response.text}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}


# Build UI using Gradio Blocks
with gr.Blocks(title="California Housing Dataset Predictor") as demo:
    gr.Markdown("## 🏠 California Housing Market Dataset Interface")
    gr.Markdown(
        "Enter sample house data in the text areas below and specify the target API endpoint."
    )

    with gr.Row():
        api_endpoint = gr.Textbox(
            label="API Endpoint URL",
            value=f"http://localhost:{API_PORT}/predict",
            scale=2,
        )

    gr.Markdown("### Input Features")

    # Feature Inputs using gr.TextArea
    with gr.Row():
        longitude = gr.TextArea(label="longitude", value="-122.23", lines=1)
        latitude = gr.TextArea(label="latitude", value="37.88", lines=1)
        housing_median_age = gr.TextArea(
            label="housingMedianAge", value="41.0", lines=1
        )

    with gr.Row():
        total_rooms = gr.TextArea(label="totalRooms", value="880.0", lines=1)
        total_bedrooms = gr.TextArea(label="totalBedrooms", value="129.0", lines=1)
        population = gr.TextArea(label="population", value="322.0", lines=1)

    with gr.Row():
        households = gr.TextArea(label="households", value="126.0", lines=1)
        median_income = gr.TextArea(label="medianIncome", value="8.3252", lines=1)
        gr.HTML("")

    submit_btn = gr.Button("Submit Data", variant="primary")

    gr.Markdown("### Model Output / Answer")
    answer_area = gr.JSON(label="API Endpoint Response")

    # Connect button click action to prediction logic
    submit_btn.click(
        fn=predict_house_value,
        inputs=[
            api_endpoint,
            longitude,
            latitude,
            housing_median_age,
            total_rooms,
            total_bedrooms,
            population,
            households,
            median_income,
        ],
        outputs=answer_area,
    )

if __name__ == "__main__":
    try:
        demo.launch(server_name="0.0.0.0", server_port=DEMO_PORT)
    except KeyboardInterrupt:
        print("\nStopping Gradio server safely...")
        demo.close()
