import gradio as gr
from scenes.manual_play import ManualPlay
from scenes.ai_play import AIPlay
from scenes.reinforcement import  Reinforcement
from ui.clear_controller import ClearController
from config import *

class AppBuilder:
    def __init__(
        self,
        manual_play: ManualPlay,
        ai_play: AIPlay,
        reinforcement: Reinforcement,
        clear_controller: ClearController,
    ):
        self.manual_play = manual_play
        self.ai_play = ai_play
        self.reinforcement = reinforcement
        self._clear_controller = clear_controller

    def build(self):
        with gr.Blocks(title="Parking Simulator") as demo:

            # 서버와 통신할 보이지 않는 데이터 창구
            state_data = gr.JSON(visible=False)

            gr.Markdown("# 주차 시뮬레이션")
            gr.Markdown(
                """
                자동차를 제한 시간 동안 화면에 보이는 주차장 영역(초록색)으로 움직여 정확히 맞추는 프로그램입니다. \\
                수동 조작 탭에서는 화면 아래의 조작 버튼을 가지고 차량을 조작할 수 있습니다.
                ↑/↓ 버튼을 눌러 전진/후진할 수 있습니다. ←/→ 버튼을 눌러 좌회전/우회전할 수 있습니다. 
                \'정지\' 버튼을 눌러 이동을 멈출 수 있습니다.\\
                제한 시간이 끝나면, 조작이 더 이상 불가능해지며, 잔여 시간과 주차의 정확성에 따라 종합 점수가 매겨집니다. 
                종합 점수에 따라 S, A, B, C의 등급이 매겨집니다. 각각에 대응하는 종합 점수는 아래와 같습니다.\\
                S: 90 ~ 100\\
                A: 80 ~ 89\\
                B: 70 ~ 79\\
                C: 0 ~ 69
                """
            )

            active_tab = gr.State("manual_play")

            with gr.Tabs():

                with gr.TabItem("수동 조작", id="manual_play") as tab_manual:
                    gr.HTML(MANUAL_HTML)
                    with gr.Column(scale=3):
                        with gr.Row():
                            btn_up = gr.Button("↑", scale=1)

                        with gr.Row():
                            btn_left = gr.Button("←")
                            btn_stop = gr.Button("정지")
                            btn_right = gr.Button("→")

                        with gr.Row():
                            btn_down = gr.Button("↓")

                    with gr.Row():
                        with gr.Column(scale=2):
                            manual_play_text_timer = gr.Markdown("0.00/0.00")
                            manual_play_text_parking = gr.Markdown("주차 중...")
                            manual_play_text_score = gr.Markdown("점수: 0")

                        with gr.Column(scale=2):
                            manual_play_text_left_time = gr.Markdown("남은 시간: 0.00")
                            manual_play_text_overall_score = gr.Markdown("종합 점수: N/A")
                            manual_play_text_grade = gr.Markdown("등급: N/A")

                    manual_play_pause_btn = gr.Button("게임 진행 중")
                    manual_play_reset_btn = gr.Button("초기화")

                with gr.TabItem("AI 조작", id="ai_play") as tab_ai:
                    gr.HTML(AI_HTML)
                    with gr.Row():
                        with gr.Column(scale=2):
                            ai_play_text_timer = gr.Markdown("0.00/0.00")
                            ai_play_text_parking = gr.Markdown("주차 중...")
                            ai_play_text_score = gr.Markdown("점수: 0")

                        with gr.Column(scale=2):
                            ai_play_text_left_time = gr.Markdown("남은 시간: 0.00")
                            ai_play_text_overall_score = gr.Markdown("종합 점수: N/A")
                            ai_play_text_grade = gr.Markdown("등급: N/A")



                    ai_play_pause_btn = gr.Button("게임 진행 중")
                    ai_play_reset_btn = gr.Button("초기화")

                with gr.TabItem("강화학습", id="reinforcement") as tab_reinforcement:
                    gr.HTML(REINFORCEMENT_HTML)
                    with gr.Row():
                        with gr.Column(scale=2):
                            reinforcement_text_timer = gr.Markdown("0.00/0.00")
                            reinforcement_text_parking = gr.Markdown("주차 중...")
                            reinforcement_text_score = gr.Markdown("점수: 0")

                        with gr.Column(scale=2):
                            reinforcement_text_left_time = gr.Markdown("남은 시간: 0.00")
                            reinforcement_text_overall_score = gr.Markdown("종합 점수: N/A")
                            reinforcement_text_grade = gr.Markdown("등급: N/A")

                    with gr.Row():
                        reinforcement_text_episode = gr.Markdown("시행 1")
                        gr.Markdown(" | ")
                        reinforcement_text_epsilon = gr.Markdown("ε = 100.00%")
                        gr.Markdown(" | ")
                        reinforcement_text_reward = gr.Markdown("보상 = ")


                    reinforcement_pause_btn = gr.Button("게임 진행 중")
                    reinforcement_reset_btn = gr.Button("초기화")
                    reinforcement_save_btn = gr.Button("저장")

            tab_manual.select(
                fn=lambda: "manual_play",
                outputs=active_tab
            )

            tab_ai.select(
                fn=lambda: "ai_play",
                outputs=active_tab
            )

            tab_reinforcement.select(
                fn=lambda: "reinforcement",
                outputs=active_tab
            )


            def update_game(current_tab, target_tab, game):
                if current_tab != target_tab:
                    return (
                        gr.skip(),
                        gr.skip(),
                        gr.skip(),
                        gr.skip(),
                        gr.skip(),
                        gr.skip(),
                        gr.skip()
                    )

                render_data = game.update()
                env = game.env

                timer_text = (
                    f"현재 시간: "
                    f"{env.elapsed_time:.2f} / {env.time_limit:.2f}"
                )

                parking_text = (
                    f"주차 중..."
                    f"({env.parking_time:.2f} / "
                    f"{env.parking_finish_time:.2f})"
                    if env.parking_time >= 0.02
                    else "주행 중..."
                )

                score_text = (
                    f"점수: {env.get_accuracy() * 100:.0f}%"
                )

                left_time_text = (
                    f"남은 시간: "
                    f"{env.time_limit - env.elapsed_time:.2f}"
                )

                overall_score = (env.parking_accuracy * 0.8 + (env.time_limit - env.elapsed_time)/env.time_limit * 0.2) * 100

                overall_score_text = (
                    f"종합 점수: {overall_score:.0f}"
                    if env.is_finished
                    else "종합 점수: N/A"
                )

                grade_color = BLACK
                grade = "N/A"
                if overall_score >= 90: grade_color = YELLOW; grade = "S"
                elif overall_score >= 80: grade_color = RED; grade = "A"
                elif overall_score >= 70: grade_color = BLUE; grade = "B"
                else: grade_color = GREEN; grade = "C"

                grade_text = "등급: N/A"
                if env.is_finished:
                    if env.finish_type == "SUCCESS":
                        grade_text = f"등급: {grade}"
                    if env.finish_type == "TIME_OVER":
                        grade_text = "시간 초과 (실패)"
                    if env.finish_type == "COLLISION":
                        grade_text = "장애물 충돌 (실패)"
                return (
                    render_data,
                    timer_text,
                    parking_text,
                    score_text,
                    left_time_text,
                    overall_score_text,
                    grade_text,
                )

            main_timer = gr.Timer(1.0 / FPS)

            main_timer.tick(
                fn=lambda current_tab:
                update_game(
                    current_tab,
                    "manual_play",
                    self.manual_play
                ),
                inputs=[active_tab],
                outputs=[
                    state_data,
                    manual_play_text_timer,
                    manual_play_text_parking,
                    manual_play_text_score,
                    manual_play_text_left_time,
                    manual_play_text_overall_score,
                    manual_play_text_grade
                ]
            ).then(
                fn=None,
                inputs=[state_data],
                js="""
                    (data) => {
                         window.drawGame("manualCanvas", data);
                    }
                    """
            )

            main_timer.tick(
                fn=lambda current_tab:
                update_game(
                    current_tab,
                    "ai_play",
                    self.ai_play
                ),
                inputs=[active_tab],
                outputs=[
                    state_data,
                    ai_play_text_timer,
                    ai_play_text_parking,
                    ai_play_text_score,
                    ai_play_text_left_time,
                    ai_play_text_overall_score,
                    ai_play_text_grade
                ]
            ).then(
                fn=None,
                inputs=[state_data],
                js="""
                    (data) => {
                         window.drawGame("aiCanvas", data);
                    }
                    """
            )

            main_timer.tick(
                fn=lambda current_tab:
                update_game(
                    current_tab,
                    "reinforcement",
                    self.reinforcement
                ),
                inputs=[active_tab],
                outputs=[
                    state_data,
                    reinforcement_text_timer,
                    reinforcement_text_parking,
                    reinforcement_text_score,
                    reinforcement_text_left_time,
                    reinforcement_text_overall_score,
                    reinforcement_text_grade
                ]
            ).then(
                fn=None,
                inputs=[state_data],
                js="""
                    (data) => {
                         window.drawGame("reinforcementCanvas",data);
                    }
                    """
            )

            def update_reinforcement_info(current_tab):
                if current_tab != "reinforcement":
                    return (
                        gr.skip(),
                        gr.skip(),
                        gr.skip(),
                    )
                episode_text = f"시행 {self.reinforcement.episode}"
                epsilon_text = f"ε = {self.reinforcement.agent.epsilon * 100:.2f}%"
                reward_text = f"보상 = {self.reinforcement.total_reward:.2f}"

                return (
                    episode_text,
                    epsilon_text,
                    reward_text
                )

            main_timer.tick(
                fn=update_reinforcement_info,
                inputs=[active_tab],
                outputs=[
                    reinforcement_text_episode,
                    reinforcement_text_epsilon,
                    reinforcement_text_reward
                ]
            )

            # 이동 버튼
            btn_up.click(
                fn=lambda: self.manual_play.control("ArrowUp"),
                inputs=None
            )

            btn_down.click(
                fn=lambda: self.manual_play.control("ArrowDown"),
                inputs=None
            )

            btn_left.click(
                fn=lambda: self.manual_play.control("ArrowLeft"),
                inputs=None
            )

            btn_right.click(
                fn=lambda: self.manual_play.control("ArrowRight"),
                inputs=None
            )

            btn_stop.click(
                fn=lambda: self.manual_play.control("STOP"),
                inputs=None
            )

            # 정지 버튼
            manual_play_pause_btn.click(
                fn=self.manual_play.toggle_pause,
                inputs=None,
                outputs=manual_play_pause_btn
            )

            ai_play_pause_btn.click(
                fn=self.ai_play.toggle_pause,
                inputs=None,
                outputs=ai_play_pause_btn
            )

            reinforcement_pause_btn.click(
                fn=self.reinforcement.toggle_pause,
                inputs=None,
                outputs=reinforcement_pause_btn
            )

            # 리셋 버튼
            manual_play_reset_btn.click(
                fn=self.manual_play.reset,
                inputs=None
            )

            ai_play_reset_btn.click(
                fn=self.ai_play.reset,
                inputs=None
            )

            reinforcement_reset_btn.click(
                fn=self.reinforcement.reset,
                inputs=None
            )

            # 저장 버튼
            reinforcement_save_btn.click(
                fn=self.reinforcement.agent.save,
                inputs=None
            )

        demo.queue(default_concurrency_limit=10)

        return demo