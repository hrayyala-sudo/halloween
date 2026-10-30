elif page == "👻 Phantom Quest":

    if st.session_state.phantom_summoned:

        st.header("👻 Phantom Quest: True or False")

        st.write("""
        The Grand Phantom has challenged you!

        Answer five true-or-false questions correctly in a row
        to escape the mansion. Choose one of the two doors:
        TRUE or FALSE.
        """)

        st.markdown(
            f"<div class='spooky-box'>"
            f"<h2>Question {st.session_state.quest_round} of 5</h2>"
            f"<h3>🏆 Correct Answers in a Row: {st.session_state.quest_score}/5</h3>"
            f"</div>",
            unsafe_allow_html=True
        )

        if st.session_state.quest_failed:

            st.error(
                "💀 Incorrect answer! Your streak has ended. "
                "The ghosts have sent you back to the beginning!"
            )

            if st.button("🔄 Try Phantom Quest Again"):

                reset_phantom_quest()
                st.rerun()

        elif st.session_state.phantom_quest_completed:

            st.success(
                "🎉 You escaped the mansion! "
                "You answered five questions correctly in a row!"
            )

            st.balloons()

            st.info(
                "🎃 A new adventure has unlocked: "
                "The Haunted Graveyard!"
            )

            if st.button("🔄 Play Phantom Quest Again"):
                reset_phantom_quest()
                st.rerun()

        else:

            current_question = st.session_state.quest_questions[
                st.session_state.quest_round - 1
            ]

            st.subheader("❓ True or False?")

            st.markdown(
                f"<div class='spooky-box'><h3>{current_question['question']}</h3></div>",
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "🚪 TRUE",
                    key=f"quest_true_{st.session_state.quest_round}",
                    use_container_width=True
                ):
                    if current_question["answer"] is True:
                        st.session_state.quest_score += 1
                        if st.session_state.quest_score == 5:
                            st.session_state.phantom_quest_completed = True
                        else:
                            st.session_state.quest_round += 1
                    else:
                        st.session_state.quest_failed = True
                    st.rerun()

            with col2:
                if st.button(
                    "🚪 FALSE",
                    key=f"quest_false_{st.session_state.quest_round}",
                    use_container_width=True
                ):
                    if current_question["answer"] is False:
                        st.session_state.quest_score += 1
                        if st.session_state.quest_score == 5:
                            st.session_state.phantom_quest_completed = True
                        else:
                            st.session_state.quest_round += 1
                    else:
                        st.session_state.quest_failed = True
                    st.rerun()

    else:

        st.error("This dimension is still locked!")
