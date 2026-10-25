import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Library System",
    page_icon="📚",
    layout="centered"
)

# ---------- SESSION STATE ----------
if "library" not in st.session_state:
    st.session_state.library = []

if "book_id" not in st.session_state:
    st.session_state.book_id = 1

if "issue_history" not in st.session_state:
    st.session_state.issue_history = []


# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.stApp {
    background-image: url("https://www.invertisuniversity.ac.in/uploads/image/20260306122238.webp");
    background-size: cover;
    background-attachment: fixed;
}

/* Watermark */
.watermark {
    position: fixed;
    bottom: 10px;
    right: 15px;
    opacity: 0.3;
    font-size: 20px;
    color: #FFFFFF;
    z-index: 999;
}

/* Main title */
.main-title {
    color: black;
    text-align: center;
    background: linear-gradient(#0066ff,#ffffff,#0033cc);
    border-radius: 10px;
    padding: 12px;
}

/* Section headings */
.section-title {
    color: black;
    background: linear-gradient(#3399ff,#66ffff,#6666ff);
    border-radius: 10px;
    padding: 8px 16px;
    display: inline-block;
}

/* Buttons */
.stButton > button {
    border-radius: 8px;
    font-weight: bold;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}
</style>

<div class="watermark">🐍 Python Streamlit App</div>
""", unsafe_allow_html=True)


# ---------- MAIN TITLE ----------
st.markdown("""
<h1 class="main-title">
    📚 LIBRARY MANAGEMENT SYSTEM
</h1>
""", unsafe_allow_html=True)

st.write("")


# ---------- MENU ----------
menu = st.sidebar.selectbox(
    ":rainbow[Menu]",
    [
        "Add Book",
        "Issue Book",
        "Return Book",
        "View Books",
        "Issue History"
    ]
)


# ---------- ADD BOOK ----------
if menu == "Add Book":

    st.markdown(
        '<h2 class="section-title">➕ Add Book</h2>',
        unsafe_allow_html=True
    )

    st.write("")

    Name = st.text_input(":rainbow[Enter Book Name]")

    Quantity = st.number_input(
        ":rainbow[Enter Quantity]",
        min_value=1,
        step=1
    )

    if st.button(":rainbow[Add Book]"):

        if not Name.strip():
            st.warning("Please enter book name.")

        else:
            existing_book = None

            # Check for an existing book
            for book in st.session_state.library:
                if book["Name"].strip().casefold() == Name.strip().casefold():
                    existing_book = book
                    break

            if existing_book:

                # Add quantity to the existing book
                existing_book["Quantity"] += int(Quantity)

                st.success(
                    f"'{existing_book['Name']}' quantity updated! "
                    f"Total quantity: {existing_book['Quantity']}"
                )

            else:

                # Add a new book
                st.session_state.library.append({
                    "Id": st.session_state.book_id,
                    "Name": Name.strip(),
                    "Quantity": int(Quantity)
                })

                st.session_state.book_id += 1

                st.success(
                    f"Book '{Name.strip()}' added successfully!"
                )


# ---------- ISSUE BOOK ----------
elif menu == "Issue Book":

    st.markdown(
        '<h2 class="section-title">📖 Issue Book</h2>',
        unsafe_allow_html=True
    )

    st.write("")

    if not st.session_state.library:

        st.info("No books available. Please add books first.")

    else:

        available_books = [
            book for book in st.session_state.library
            if book["Quantity"] > 0
        ]

        if not available_books:

            st.error("All books are currently out of stock.")

        else:

            # Select a book from the dropdown
            book_options = {
                f"{book['Name']} (Available: {book['Quantity']})": book["Id"]
                for book in available_books
            }

            selected_book = st.selectbox(
                ":rainbow[Select Book]",
                list(book_options.keys())
            )

            selected_id = book_options[selected_book]

            book = next(
                b for b in st.session_state.library
                if b["Id"] == selected_id
            )

            st.info(
                f"Available quantity: {book['Quantity']}"
            )

            issue_quantity = st.number_input(
                ":rainbow[How many books do you want to issue?]",
                min_value=1,
                max_value=int(book["Quantity"]),
                value=1,
                step=1
            )

            borrower = st.text_input(
                ":rainbow[Enter Student Name]"
            )

            if st.button(":rainbow[Issue Book]"):

                if not borrower.strip():

                    st.warning("Please enter student name.")

                elif issue_quantity > book["Quantity"]:

                    st.error("Not enough books available.")

                else:

                    # Decrease available stock
                    book["Quantity"] -= int(issue_quantity)

                    # Save issue history
                    st.session_state.issue_history.append({
                        "Book ID": book["Id"],
                        "Book Name": book["Name"],
                        "Student Name": borrower.strip(),
                        "Issued Quantity": int(issue_quantity)
                    })

                    st.success(
                        f"{issue_quantity} copies of "
                        f"'{book['Name']}' issued successfully!"
                    )

                    st.info(
                        f"Remaining quantity: {book['Quantity']}"
                    )


# ---------- RETURN BOOK ----------
elif menu == "Return Book":

    st.markdown(
        '<h2 class="section-title">🔄 Return Book</h2>',
        unsafe_allow_html=True
    )

    st.write("")

    if not st.session_state.library:

        st.info("No books available in the library.")

    else:

        book_options = {
            f"{book['Name']} (ID: {book['Id']})": book["Id"]
            for book in st.session_state.library
        }

        selected_book = st.selectbox(
            ":rainbow[Select Book]",
            list(book_options.keys())
        )

        selected_id = book_options[selected_book]

        book = next(
            b for b in st.session_state.library
            if b["Id"] == selected_id
        )

        return_quantity = st.number_input(
            ":rainbow[How many books do you want to return?]",
            min_value=1,
            step=1,
            value=1
        )

        if st.button(":rainbow[Return Book]"):

            book["Quantity"] += int(return_quantity)

            st.success(
                f"{return_quantity} copies of "
                f"'{book['Name']}' returned successfully!"
            )

            st.info(
                f"Updated quantity: {book['Quantity']}"
            )


# ---------- VIEW BOOKS ----------
elif menu == "View Books":

    st.markdown(
        '<h2 class="section-title">📋 Book List</h2>',
        unsafe_allow_html=True
    )

    st.write("")

    if len(st.session_state.library) == 0:

        st.info(":rainbow[No books available]")

    else:

        df = pd.DataFrame(st.session_state.library)

        df = df.set_index("Id")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total Book Titles",
                len(st.session_state.library)
            )

        with col2:
            st.metric(
                "Available Copies",
                sum(
                    book["Quantity"]
                    for book in st.session_state.library
                )
            )


# ---------- ISSUE HISTORY ----------
elif menu == "Issue History":

    st.markdown(
        '<h2 class="section-title">📚 Issue History</h2>',
        unsafe_allow_html=True
    )

    st.write("")

    if not st.session_state.issue_history:

        st.info("No books have been issued yet.")

    else:

        history_df = pd.DataFrame(
            st.session_state.issue_history
        )

        st.dataframe(
            history_df,
            use_container_width=True
        )

        total_issued = sum(
            item["Issued Quantity"]
            for item in st.session_state.issue_history
        )

        st.metric(
            "Total Copies Issued",
            total_issued
        )