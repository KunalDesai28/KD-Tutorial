import streamlit as st
from firebase_admin import firestore

def app():
    db = firestore.client()

    # Ensure the user is logged in
    if 'username' not in st.session_state or not st.session_state['username']:
        st.warning('Please login first to view your posts.')
        return

    st.title(f"Your Posts - {st.session_state['username']}")

    try:
        # Fetch the user's posts
        result = db.collection('Posts').document(st.session_state['username']).get()
        user_data = result.to_dict()
        content = user_data.get('content', [])

        if not content:
            st.info("You don't have any posts yet!")
            return

        # Function to delete a post
        def delete_post(index):
            post_to_delete = content[index]
            try:
                # Remove the post from Firestore
                db.collection('Posts').document(st.session_state['username']).update(
                    {"content": firestore.ArrayRemove([post_to_delete])}
                )
                st.success('Post deleted successfully.')
                st.experimental_rerun()  # Refresh the page after deletion
            except Exception as e:
                st.error(f"An error occurred while deleting the post: {e}")

        # Display posts with delete buttons
        for index, post in enumerate(content):
            with st.container():
                st.markdown(
                    f"""
                    <div style="padding: 10px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px;">
                        <p style="margin: 0; font-size: 16px; color: #333;">{post}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.button(
                    "Delete Post",
                    key=f"delete_button_{index}",
                    on_click=delete_post,
                    args=(index,),
                )

    except Exception as e:
        st.error(f"An unexpected error occurred. Please try again later.")

