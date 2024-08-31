import streamlit as st
import re

st.set_page_config(
    page_title="計算機",
    page_icon="favicon.png"
)


def app():
    st.title('計算機')

    # セッション状態の初期化
    if 'display' not in st.session_state:
        st.session_state.display = '0'
    if 'result_shown' not in st.session_state:
        st.session_state.result_shown = False

    # 表示
    st.header(st.session_state.display)

    def calculate(expression):
        try:
            # 数字、小数点、演算子以外の文字を削除
            clean_expr = re.sub(r'[^0-9+\-*/.]', '', expression)

            # 式を数字と演算子に分割
            parts = re.split(r'([+\-*/])', clean_expr)

            # 空の文字列を削除
            parts = [part for part in parts if part]

            result = float(parts[0])
            for i in range(1, len(parts), 2):
                operator = parts[i]
                operand = float(parts[i+1])
                if operator == '+':
                    result += operand
                elif operator == '-':
                    result -= operand
                elif operator == '*':
                    result *= operand
                elif operator == '/':
                    if operand == 0:
                        return 'エラー: ゼロ除算'
                    result /= operand

            # 結果が整数の場合は整数として表示
            if result.is_integer():
                return str(int(result))
            else:
                return f"{result:.10f}".rstrip('0').rstrip('.')
        except ValueError:
            return '計算失敗'
        except Exception as e:
            return f'エラー: {str(e)}'

    # ボタンクリックハンドラ
    def button_click(button):
        if st.session_state.result_shown:
            if button in '0123456789':
                st.session_state.display = button
            elif button in '+-*/':
                st.session_state.display += button
            st.session_state.result_shown = False
        else:
            if st.session_state.display == '0' and button not in '+-*/':
                st.session_state.display = button
            else:
                st.session_state.display += button

        if button == 'C':
            st.session_state.display = '0'
            st.session_state.result_shown = False
        elif button == '=':
            st.session_state.display = calculate(st.session_state.display)
            st.session_state.result_shown = True

    # ボタンレイアウトの作成
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.button('7', on_click=button_click, args=('7',))
        st.button('4', on_click=button_click, args=('4',))
        st.button('1', on_click=button_click, args=('1',))
        st.button('0', on_click=button_click, args=('0',))

    with col2:
        st.button('8', on_click=button_click, args=('8',))
        st.button('5', on_click=button_click, args=('5',))
        st.button('2', on_click=button_click, args=('2',))
        st.button('.', on_click=button_click, args=('.',))

    with col3:
        st.button('9', on_click=button_click, args=('9',))
        st.button('6', on_click=button_click, args=('6',))
        st.button('3', on_click=button_click, args=('3',))
        st.button('=', on_click=button_click, args=('=',))

    with col4:
        st.button('➗', on_click=button_click, args=('/',))
        st.button('✖️', on_click=button_click, args=('*',))
        st.button('➖', on_click=button_click, args=('-',))
        st.button('➕', on_click=button_click, args=('+',))

    with col1:
        st.button('C', on_click=button_click, args=('C',))


if __name__ == '__main__':
    app()
