import os
import boto3
from flask import Flask, jsonify

app = Flask(__name__)

# Config
REGION = os.environ.get("AWS_REGION", "ap-south-2")

# DynamoDB
dynamodb = boto3.resource("dynamodb", region_name=REGION)
courses_table = dynamodb.Table("courses-amruthesh")


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "course-service"}), 200


# 🔥 GET single course
@app.route("/courses/<course_id>", methods=["GET"])
def get_course(course_id):
    try:
        resp = courses_table.get_item(Key={"id": course_id})
        item = resp.get("Item")

        if not item:
            return jsonify({"error": "Course not found"}), 404

        return jsonify(item), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


# 🔥 GET all courses
@app.route("/courses", methods=["GET"])
def list_courses():
    try:
        resp = courses_table.scan(Limit=50)
        return jsonify(resp.get("Items", [])), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=False)