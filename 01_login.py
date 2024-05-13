import streamlit as st
import pages 

# User data (for demonstration purposes)
user_data = {
    'user1': {'password': 'pass1', 'data': 'User 1 Data'},
    'user2': {'password': 'pass2', 'data': 'User 2 Data'},
    # Add data for other users
}
if 'username' not in st.session_state:
    st.session_state.username = None

def login():
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    
    if st.session_state.username is None:
        st.title('Login')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            if username in user_data:
                if user_data[username]['password'] == password:
                    st.session_state['username'] = username
                    return username
                else:
                    st.error('Incorrect password')
            else:
                st.error('User not found')
    else:
        return st.session_state.username

def main():
    username = login()
    if username:
        st.write(f'Welcome, {username}!')
        st.write(f'Your data: {user_data[username]["data"]}')
    else:
        st.warning('Please login to access the content')

if __name__ == "__main__":
    main()
