import streamlit as st

# Mapeamentos de fiação (wiring) para os rotores e o refletor
# A-Z -> outro caractere
ROTOR_WIRING = {
    "I":   "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II":  "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
    "IV":  "ESOVPZJAYQUIRXHMCTPNFVWKBL",
    "V":   "VZBRGITYUPSDNHLXAWMJQOFECK"
}

# A-Z -> outro caractere
REFLECTOR_WIRING = {
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT"
}

# Posições dos entalhes (notch) para o movimento do próximo rotor
# O rotor avança o próximo quando ele próprio atinge o entalhe
ROTOR_NOTCHES = {
    "I":   "Q",
    "II":  "E",
    "III": "V",
    "IV":  "J",
    "V":   "Z"
}

class Rotor:
    """
    Representa um rotor da máquina Enigma.
    """
    def __init__(self, wiring, notch, position):
        self.wiring = wiring
        self.notch = notch
        self.position = ord(position.upper()) - ord('A')
        self.forward_map = {chr(i + ord('A')): self.wiring[i] for i in range(26)}
        self.backward_map = {self.wiring[i]: chr(i + ord('A')) for i in range(26)}

    def rotate(self):
        """
        Gira o rotor em uma posição.
        """
        self.position = (self.position + 1) % 26
        return self.position_char() == self.notch

    def position_char(self):
        """
        Retorna a letra da posição atual do rotor.
        """
        return chr(self.position + ord('A'))

    def encrypt_forward(self, char):
        """
        Criptografa um caractere na direção de entrada do rotor.
        """
        idx = (ord(char) - ord('A') + self.position) % 26
        encrypted_char = self.forward_map[chr(idx + ord('A'))]
        return chr((ord(encrypted_char) - ord('A') - self.position + 26) % 26 + ord('A'))

    def encrypt_backward(self, char):
        """
        Criptografa um caractere na direção de saída do rotor.
        """
        idx = (ord(char) - ord('A') + self.position) % 26
        encrypted_char = self.backward_map[chr(idx + ord('A'))]
        return chr((ord(encrypted_char) - ord('A') - self.position + 26) % 26 + ord('A'))

class Reflector:
    """
    Representa o refletor da máquina Enigma.
    """
    def __init__(self, wiring):
        self.wiring = wiring
        self.map = {chr(i + ord('A')): self.wiring[i] for i in range(26)}

    def reflect(self, char):
        """
        Reflete um caractere.
        """
        return self.map[char]

class EnigmaMachine:
    """
    Simula a máquina Enigma completa.
    """
    def __init__(self, rotor1_type, rotor2_type, rotor3_type, pos1, pos2, pos3):
        self.rotor1 = Rotor(ROTOR_WIRING[rotor1_type], ROTOR_NOTCHES[rotor1_type], pos1)
        self.rotor2 = Rotor(ROTOR_WIRING[rotor2_type], ROTOR_NOTCHES[rotor2_type], pos2)
        self.rotor3 = Rotor(ROTOR_WIRING[rotor3_type], ROTOR_NOTCHES[rotor3_type], pos3)
        self.reflector = Reflector(REFLECTOR_WIRING["B"])

    def encrypt_char(self, char):
        """
        Criptografa um único caractere.
        """
        # Rotaciona os rotores
        # O rotor 1 sempre gira
        should_rotate2 = self.rotor1.rotate()
        # O rotor 2 gira se o rotor 1 atingir o entalhe
        should_rotate3 = should_rotate2 and self.rotor2.rotate()
        # O rotor 3 gira se o rotor 2 atingir o entalhe
        if should_rotate3:
            self.rotor3.rotate()
        
        # O sinal passa pelos rotores (da direita para a esquerda)
        encrypted = self.rotor1.encrypt_forward(char)
        encrypted = self.rotor2.encrypt_forward(encrypted)
        encrypted = self.rotor3.encrypt_forward(encrypted)

        # O sinal é refletido
        encrypted = self.reflector.reflect(encrypted)

        # O sinal volta pelos rotores (da esquerda para a direita)
        encrypted = self.rotor3.encrypt_backward(encrypted)
        encrypted = self.rotor2.encrypt_backward(encrypted)
        encrypted = self.rotor1.encrypt_backward(encrypted)
        
        return encrypted

def app():
    """
    Aplica-se a interface de usuário do Streamlit para a Máquina Enigma.
    """
    st.title("🛡️ Simulador da Máquina Enigma")
    st.markdown("---")

    ## O Papel dos Rotadores
    st.header("O Papel dos Rotadores")
    st.write("""
    Os **rotadores** são o coração da máquina Enigma. Eles são discos com 26 posições, cada um com uma fiação interna que embaralha as 26 letras do alfabeto. O que torna a Enigma tão complexa é que a fiação muda a cada letra digitada.

    1.  **Fiação Interna:** Cada rotor tem uma fiação fixa que mapeia cada letra de entrada para uma letra de saída diferente.
    2.  **Movimento:** O rotor mais à direita avança uma posição a cada vez que uma tecla é pressionada.
    3.  **Mecanismo de Carregamento:** Quando um rotor atinge um ponto específico (o **entalhe**), ele empurra o rotor à sua esquerda, fazendo-o girar também. Este mecanismo de cascata cria uma permutação gigantesca de combinações, tornando a cifra extremamente difícil de quebrar.
    """)
    st.markdown("---")

    ## Configuração da Máquina
    st.header("Configuração da Máquina")
    rotor_options = list(ROTOR_WIRING.keys())
    
    st.write("Escolha três rotores para a máquina. A ordem é importante (da esquerda para a direita).")
    col1, col2, col3 = st.columns(3)
    with col1:
        rotor3_choice = st.selectbox("Rotor 1 (Esquerda)", rotor_options, index=2)
    with col2:
        rotor2_choice = st.selectbox("Rotor 2 (Meio)", rotor_options, index=1)
    with col3:
        rotor1_choice = st.selectbox("Rotor 3 (Direita)", rotor_options, index=0)

    st.write("Defina a posição inicial de cada rotor (A-Z).")
    col4, col5, col6 = st.columns(3)
    with col4:
        pos3_choice = st.text_input("Posição 1", "A", max_chars=1)
    with col5:
        pos2_choice = st.text_input("Posição 2", "A", max_chars=1)
    with col6:
        pos1_choice = st.text_input("Posição 3", "A", max_chars=1)
    
    st.markdown("---")

    ## Criptografar Mensagem
    st.header("Criptografar Mensagem")
    texto_entrada = st.text_area("Digite o texto a ser criptografado:", height=150)
    
    if st.button("Criptografar"):
        if texto_entrada:
            # Converte para maiúsculas e remove caracteres não alfabéticos
            texto_limpo = ''.join(filter(str.isalpha, texto_entrada.upper()))

            if not texto_limpo:
                st.warning("Por favor, digite pelo menos uma letra para criptografar.")
            else:
                try:
                    # Instancia a máquina Enigma com as configurações do usuário
                    enigma = EnigmaMachine(rotor1_choice, rotor2_choice, rotor3_choice, pos1_choice, pos2_choice, pos3_choice)
                    
                    texto_saida = ""
                    for char in texto_limpo:
                        texto_saida += enigma.encrypt_char(char)
                    
                    st.subheader("Mensagem Criptografada")
                    st.success(texto_saida)
                except KeyError:
                    st.error("Por favor, insira posições iniciais válidas (uma letra de A a Z).")
