import streamlit as st
from firebase_admin import firestore


def app():
    if 'db' not in st.session_state:
        st.session_state.db = ''

    db = firestore.client()
    st.session_state.db = db
    st.title('    :violet[KD]   :sunglasses:')

    ph = 'Login to be able to Post!!' if st.session_state.username == '' else 'Post your Thought'
    post = st.text_area(label='  :orange[+ New Post]', placeholder=ph, height=None, max_chars=500, key="new_post")

    if st.button('Post', use_container_width=True):
        if post != '':
            info = db.collection('Posts').document(st.session_state.username).get()
            if info.exists:
                info = info.to_dict()
                if 'Content' in info.keys():
                    pos = db.collection('Posts').document(st.session_state.username)
                    pos.update({u'Content': firestore.ArrayUnion([post])})
                else:
                    data = {"Content": [post], 'Username': st.session_state.username}
                    db.collection('Posts').document(st.session_state.username).set(data)
            else:
                data = {"Content": [post], 'Username': st.session_state.username}
                db.collection('Posts').document(st.session_state.username).set(data)

            st.success('Post Uploaded')

    st.header(' :violet[Latest Posts] ')

    docs = db.collection('Posts').get()
    for i, doc in enumerate(docs):
        d = doc.to_dict()
        try:
            st.text_area(
                label=f':green[Posted by:] {d["Username"]}',
                value=d['Content'][-1],
                height=68,
                key=f"post_{i}"  # Unique key for each text_area
            )
        except Exception as e:
            st.error(f"Error displaying post: {e}")
