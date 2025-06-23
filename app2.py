import streamlit as st
from pymongo import MongoClient
from bson import ObjectId

# MongoDB Connection
client = MongoClient('mongodb+srv://arman:arman123@project.lsbywbi.mongodb.net/', tlsAllowInvalidCertificates=True)
db = client["movieslist"]
movies_collection = db["list"]

st.title("🎥 Movies Manager")

st.subheader("➕ Add New Movie")
with st.form("add_movie_form"):
    movie_name = st.text_input("Movie Name")
    movie_time = st.text_input("Movie Time (e.g., 12:34)")
    add_btn = st.form_submit_button("Add Movie")
    if add_btn:
        if movie_name and movie_time:
            movies_collection.insert_one({"name": movie_name, "time": movie_time})
            st.success("Movie added successfully!")
        else:
            st.error("Please provide both movie name and movie time.")



st.subheader("📄 View Saved Movies")
if st.button("📂 Show Movies"):
    movies = list(movies_collection.find({}))
    if movies:
        for movie in movies:
            st.write(f"**ID:** {movie['_id']}")
            st.write(f"**Name:** {movie['name']}")
            st.write(f"**Time:** {movie['time']}")
            st.markdown("---")
    else:
        st.info("No Movies found.")


st.subheader("✏️ Update Movie")
with st.form("update_video_form"):
    movie_id_update = st.text_input("Enter Video ID to Update")
    updated_movie_name = st.text_input("New Video Name")
    updated_movie_time = st.text_input("New Video Time")
    update_btn = st.form_submit_button("Update Video")
    if update_btn:
        try:
            result = movies_collection.update_one(
                {"_id": ObjectId(movie_id_update)},
                {"$set": {"name": updated_movie_name, "time": updated_movie_time}}
            )
            if result.modified_count:
                st.success("Movie updated successfully.")
            else:
                st.warning("No Movies found or no changes made.")
        except Exception as e:
            st.error(f"Error: {e}")


st.subheader("❌ Delete Movies")
with st.form("delete_movie_form"):
    movie_id_delete = st.text_input("Enter Video ID to Delete")
    delete_btn = st.form_submit_button("Delete Video")
    if delete_btn:
        try:
            result = movies_collection.delete_one({"_id": ObjectId(movie_id_delete)})
            if result.deleted_count:
                st.success("Movie deleted successfully.")
            else:
                st.warning("Movie not found.")
        except Exception as e:
            st.error(f"Error: {e}")
