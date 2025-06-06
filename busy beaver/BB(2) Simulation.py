from manim import *

# 전이 함수 정의
def transition(state, symbol):
    transitions = {
        'A': {'0': ('1', 'R', 'B'), '1': ('1', 'L', 'B')},
        'B': {'0': ('1', 'L', 'A'), '1': ('1', 'R', 'H')},
    }
    return transitions.get(state, {}).get(symbol, (symbol, 'S', 'H'))  # 기본값: 종료 상태로 이동

# 전이 함수를 통해 테이프 동작 계산
def compute_tape(steps=20):
    tape = ['0'] * steps  # 초기 테이프 설정 (모두 '0'으로 시작)
    state = 'A'
    head_position = steps // 2  # 초기 헤드 위치는 중간
    actions = []  # 각 스텝의 상태, 테이프 내용, 헤드 위치 기록

    # 튜링 머신 시뮬레이션
    while state != 'H' and 0 <= head_position < len(tape):
        current_symbol = tape[head_position]
        symbol, direction, new_state = transition(state, current_symbol)
        
        # 테이프 업데이트 및 기록 저장
        tape[head_position] = symbol
        actions.append((list(tape), head_position, state, direction, new_state))

        # 헤드 위치 업데이트
        if direction == 'R':
            head_position += 1
        elif direction == 'L':
            head_position -= 1
        
        # 상태 업데이트
        state = new_state

    return actions

class BB2Simulation(Scene):
    def construct(self):
        move_count = 0

        # 튜링 머신 시뮬레이션 결과 계산
        actions = compute_tape(steps=20)

        # 타이틀
        title = Text("BB(2) Simulation", font_size=42)
        title.to_edge(UP, buff=0.5)

        # 테이프 셀 초기화 및 초기 설정 유지
        tape_cells = VGroup(*[Square().scale(0.6) for _ in range(20)])
        tape_cells.arrange(RIGHT, buff=0.05)
        tape_cells.shift(DOWN * 1.5)

        # 초기 테이프 값 표시
        tape_labels = VGroup(*[Text("0", font_size=32) for _ in range(20)])
        for cell, label in zip(tape_cells, tape_labels):
            label.move_to(cell)

        # 헤드 초기 설정
        head = Triangle().scale(0.3).set_fill(RED, opacity=0).set_stroke(RED, width=3)
        head.next_to(tape_cells[10], UP, buff=0.1)

        # 상태 및 기타 텍스트 초기 설정
        state_text = Text("State: A", font_size=28, color=WHITE)
        read_text = Text("Read: 0", font_size=28, color=WHITE)
        state_text.next_to(title, DOWN, buff=1.5)
        read_text.next_to(state_text, DOWN)
        ones_text = Text("Number of ones: 0", font_size=28, color=WHITE)
        moves_text = Text("Move: 0", font_size=28, color=WHITE)
        ones_text.next_to(state_text, LEFT, buff=2)
        moves_text.next_to(ones_text, DOWN)

        # 전이 테이블 생성 및 초기 애니메이션 설정
        table_data = [["0", "1RB", "1LA"], ["1", "1LB", "1RH"]]
        table = Table(table_data, col_labels=[Tex(r"$\delta$"), Text("A"), Text("B")], include_outer_lines=True)
        table.scale(0.5)
        table.next_to(state_text, RIGHT, buff=2)

        # 초기 요소 애니메이션
        self.play(Write(title))
        self.play(Write(state_text), Write(read_text), Write(ones_text), Write(moves_text), Create(tape_cells), Write(tape_labels), Create(table))
        self.play(FadeIn(head))

        highlight_box = SurroundingRectangle(table.get_cell((2, 2)), color=RED)
        self.play(FadeIn(highlight_box))

        # 나머지 계산된 결과에 따라 애니메이션 적용
        for tape, pos, state, direction, new_state in actions:
            # 테이프의 모든 셀 업데이트 및 1의 개수 애니메이션을 동시에 실행
            new_tape_labels = VGroup()
            for i, symbol in enumerate(tape):
                new_label = Text(symbol, font_size=32).move_to(tape_cells[i])
                new_tape_labels.add(new_label)
            ones_count = tape.count('1')
            new_ones_text = Text(f"Number of ones: {ones_count}", font_size=28, color=WHITE).next_to(state_text, LEFT, buff=2)
            self.play(ReplacementTransform(tape_labels, new_tape_labels), ReplacementTransform(ones_text, new_ones_text))
            tape_labels, ones_text = new_tape_labels, new_ones_text

            # 헤드 이동 및 move 카운트 업데이트를 동시에 실행
            move_count += 1
            new_moves_text = Text(f"Move: {move_count}", font_size=28, color=WHITE).next_to(ones_text, DOWN)
            next_pos = pos + 1 if direction == 'R' else pos - 1
            head_move_animation = head.animate.next_to(tape_cells[next_pos], UP, buff=0.1) if 0 <= next_pos < len(tape_cells) else FadeOut(head)
            self.play(head_move_animation, ReplacementTransform(moves_text, new_moves_text))
            moves_text = new_moves_text

            # 상태 및 읽은 기호 텍스트 업데이트
            new_state_text = Text(f"State: {new_state}", font_size=28, color=WHITE).next_to(title, DOWN, buff=1.5)
            self.play(ReplacementTransform(state_text, new_state_text))
            state_text = new_state_text

            current_symbol = tape[next_pos] if 0 <= next_pos < len(tape) else '0'
            new_read_text = Text(f"Read: {current_symbol}", font_size=28, color=WHITE).next_to(state_text, DOWN)
            self.play(ReplacementTransform(read_text, new_read_text))
            read_text = new_read_text

            # 테두리 강조 업데이트
            row = 2 if current_symbol == '0' else 3
            col = 2 if new_state == 'A' else 3
            if new_state == 'H':
                self.play(FadeOut(highlight_box))
                break
            else:
                new_highlight_box = SurroundingRectangle(table.get_cell((row, col)), color=RED)
                self.play(ReplacementTransform(highlight_box, new_highlight_box))
                highlight_box = new_highlight_box

        # 종료 시 헤드 내부 채우기 및 상태 H로 전환
        self.play(head.animate.set_fill(RED, opacity=1))
        final_state_text = Text("State: H", font_size=28, color=WHITE).next_to(title, DOWN, buff=1.5)
        self.play(ReplacementTransform(state_text, final_state_text))
        self.wait(3)
