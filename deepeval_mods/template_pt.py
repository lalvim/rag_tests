class SynthesizerTemplate:
    @staticmethod
    def generate_synthetic_inputs(context, max_goldens_per_context):
        return f"""Quero que você atue como um redator. Com base no contexto fornecido, que é uma lista de strings, por favor gere uma lista de objetos JSON com uma chave `input`.
            O `input` pode ser uma pergunta ou uma afirmação que possa ser abordada pelo contexto fornecido.

            **
            IMPORTANTE: Certifique-se de retornar apenas no formato JSON, com a chave 'data' como uma lista de objetos JSON.
            VOCÊ DEVE TENTAR gerar {max_goldens_per_context} pontos de dados, a menos que o `input` esteja se tornando repetitivo.

            Exemplo de contexto: ["Einstein ganhou o Prêmio Nobel por sua descoberta da penicilina.", "Einstein ganhou o Prêmio Nobel em 1968."]
            Exemplo de máximos pontos de dados por contexto: 2
            Exemplo JSON:
            {{
                "data": [
                    {{
                        "input": "Pelo que Einstein era conhecido?"
                    }},
                    {{
                        "input": "Einstein era um cara inteligente, né"
                    }}
                ]  
            }}


            Você NÃO deve incorporar nenhum conhecimento prévio que você tenha e deve considerar cada contexto como verdadeiro.
            VOCÊ DEVE incluir pelo menos uma afirmação como o input.
            `input` DEVE ser uma STRING.
            VOCÊ DEVE TENTAR gerar {max_goldens_per_context} pontos de dados, a menos que o `input` gerado esteja se tornando repetitivo.
            **

            Máximos Pontos de Dados Por Contexto:
            {max_goldens_per_context}

            Contexto:
            {context}

            JSON:
            """

    @staticmethod
    def generate_synthetic_expected_output(input, context):
        return f"""Dado o input, que pode ou não ser uma pergunta, gere uma resposta usando as informações apresentadas no contexto.

**
IMPORTANTE: Certifique-se de gerar uma resposta concisa e direta ao ponto, e utilize informações de suporte no contexto.
**

Contexto:
{context}

Input:
{input}

Resposta Gerada:
"""

class EvolutionTemplate:

    base_instruction = """Quero que você atue como um reformulador de input.
    Seu objetivo é reformular um `input` dado e deve ser factualmente correto de acordo com as informações de suporte em `Contexto`.
    VOCÊ DEVE complicar o `Input` dado usando o seguinte método:"""

    @staticmethod
    def multi_context_evolution(input, context):
        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. `Input` deve ser reformulado para exigir que os leitores usem informações de todos os elementos de `Contexto`. 
            2. `Input Reformulado` deve ser completamente respondível a partir das informações em `Contexto`. 
            3. `Input Reformulado` deve ser conciso e compreensível por humanos.
            4. `Input Reformulado` não deve conter frases como 'com base no contexto fornecido' ou 'de acordo com o contexto'.
            5. `Input Reformulado` não deve conter mais de 15 palavras. Use abreviações sempre que possível.
            
            **
            EXEMPLOS

            Exemplo de contexto:
            ["Vacinas introduzem uma forma enfraquecida ou morta do patógeno no corpo humano.", "Essa exposição ajuda o sistema imunológico a aprender a reconhecer e combater o patógeno no futuro."]
            Exemplo de input:
            Como funcionam as vacinas?
            Exemplo de input reformulado:
            Como a introdução de um patógeno modificado prepara o sistema imunológico para encontros futuros?

            --------------------------
            
            Exemplo de contexto:
            ["As plantas realizam fotossíntese, usando a luz solar para converter dióxido de carbono e água em glicose e oxigênio.", "A clorofila nas folhas das plantas absorve a luz solar, iniciando o processo de fotossíntese.", "O oxigênio é um subproduto do processo de fotossíntese e é liberado na atmosfera."]
            Exemplo de input:
            Explique como as plantas produzem oxigênio.
            Exemplo de input reformulado: 
            Considerando o papel da clorofila na absorção de luz solar e na fotossíntese, como o oxigênio é produzido e liberado pelas plantas?

            --------------------------

            Exemplo de contexto:
            ["A atração gravitacional da lua sobre a Terra influencia as marés.", "A posição do sol em relação à Terra e à lua também afeta padrões de marés."]
            Exemplo de input:
            Fale sobre as marés altas.
            Exemplo de input reformulado:
            Explique como os efeitos gravitacionais combinados da lua e da posição relativa do sol influenciam os fenômenos de marés da Terra.
            **

            Contexto:
            {context}
            Input:
            {input}
            Input Reformulado:            
            """
        )

    @staticmethod
    def reasoning_evolution(input, context):
        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. Se `Input` pode ser resolvido com apenas alguns processos de pensamento simples, você pode reescrevê-lo para solicitar explicitamente raciocínio em vários passos.
            2. `Input Reescrito` deve exigir que os leitores façam múltiplas conexões lógicas ou inferências.
            3. `Input Reescrito` deve ser conciso e compreensível pelos humanos.
            4. `Input Reescrito` não deve conter frases como 'com base no contexto fornecido' ou 'de acordo com o contexto'.
            5. `Input Reescrito` deve ser totalmente respondível a partir das informações no `Contexto`.
            6. `Input Reescrito` não deve conter mais de 15 palavras. Use abreviações sempre que possível.

            **
            EXEMPLOS

            Exemplo de contexto:
            A clorofila permite que as plantas absorvam energia da luz, e essa energia é usada para converter dióxido de carbono e água em glicose e oxigênio, um processo conhecido como fotossíntese.
            Exemplo de input:
            Por que as plantas são verdes?
            Exemplo de input reescrito:
            Como o papel da clorofila na absorção de luz se relaciona com a cor verde das plantas e sua capacidade de produzir glicose?

            --------------------------
            
            Exemplo de contexto:
            O efeito estufa ocorre quando a atmosfera da Terra retém radiação solar, causada por gases como dióxido de carbono, metano e vapor d'água. Esse processo mantém a temperatura do planeta, mas pode levar ao aumento das temperaturas globais quando exacerbado pelas atividades humanas.
            Exemplo de input:
            O que causa a mudança das estações?
            Exemplo de input reescrito:
            Dado o aprisionamento de radiação solar pelos gases atmosféricos, explique como a atividade intensificada afeta o clima da Terra.

            --------------------------

            Exemplo de contexto:
            Teorias econômicas sugerem que a demanda e a oferta de mercado determinam os preços, mas as políticas governamentais também podem influenciar a dinâmica do mercado por meio de regulamentações, impostos e subsídios.
            Exemplo de input:
            Identifique os principais fatores que determinam o preço dos produtos em um mercado.
            Exemplo de input reescrito:
            Examine como a interação entre demanda de mercado, dinâmica de oferta e intervenções políticas do governo moldam coletivamente o mecanismo de fixação de preços dos produtos dentro de um ecossistema de mercado.
            **

            Contexto:
            {context}
            Input:
            {input}
            Input Reescrito:
            """
        )

    @staticmethod
    def concretizing_evolution(input, context):
        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. Reescreva o `Input` substituindo conceitos/questões gerais por mais específicos.
            2. O `Input` reescrito deve ser conciso e compreensível por humanos.
            3. O `Input` reescrito não deve conter frases como 'com base no contexto fornecido' ou 'de acordo com o contexto'.
            4. O `Input` reescrito deve ser completamente respondível a partir das informações no `Contexto`.
            5. O `Input` reescrito não deve conter mais do que 15 palavras. Use abreviações sempre que possível.

            **
            EXEMPLOS
            Exemplo de contexto:
            As florestas tropicais abrigam mais da metade das espécies de plantas e animais do mundo, tornando-as essenciais para a manutenção da biodiversidade global. A variedade de vida encontrada nesses ecossistemas contribui para a diversidade genética, que é crucial para a adaptação e sobrevivência em meio a condições ambientais em mudança. Essa biodiversidade também apoia a resiliência dos ecossistemas, permitindo que as florestas se recuperem de perturbações.
            A biodiversidade nas florestas tropicais desempenha um papel significativo no bem-estar humano, fornecendo serviços essenciais como purificação do ar e da água, controle de doenças e polinização de cultivos. Além disso, muitos medicamentos são derivados de plantas da floresta tropical, destacando a importância desses ecossistemas para a pesquisa médica e a saúde.
            Exemplo de input: 
            Por que a biodiversidade das florestas tropicais é importante?
            Exemplo de input reescrito:
            Como a extensa biodiversidade encontrada nas florestas tropicais, abrangendo mais da metade das espécies de plantas e animais do mundo, contribui para a manutenção da biodiversidade global, e qual é o papel dessa diversidade em aumentar a resiliência dos ecossistemas, a saúde humana por meio do controle de doenças, a polinização de cultivos e o desenvolvimento de medicamentos derivados de plantas da floresta tropical?

            --------------------------

            Exemplo de contexto:
            As abelhas desempenham um papel fundamental na polinização de plantas com flores, incluindo muitas frutas e vegetais, contribuindo para a diversidade da vida vegetal e a produção de cultivos. Sua atividade apoia o crescimento de árvores, flores e outras plantas, que servem como alimento e abrigo para inúmeros animais, mantendo assim o equilíbrio do ecossistema.
            Além de seu impacto nas culturas alimentares, as abelhas contribuem para o crescimento de plantas selvagens polinizando uma ampla variedade de plantas fora de ambientes agrícolas. Essa polinização é vital para a reprodução de muitas plantas, afetando a saúde e a sustentabilidade de ecossistemas inteiros.
            Exemplo de input: 
            Qual é o papel das abelhas nos ecossistemas?
            Exemplo de input reescrito:
            Como as abelhas, por meio de sua polinização de plantas com flores, incluindo uma infinidade de frutas e vegetais, influenciam significativamente a diversidade da vida vegetal e a produtividade agrícola, e de que maneiras suas atividades se estendem além de ambientes agrícolas para apoiar o crescimento de árvores, flores e outras plantas, fornecendo recursos essenciais para várias espécies animais e contribuindo para o equilíbrio geral e a sustentabilidade dos ecossistemas?

            --------------------------

            Exemplo de contexto:
            A geração de energia solar depende de células fotovoltaicas para converter a luz solar em eletricidade. Essas células são feitas de materiais que exibem o efeito fotovoltaico, que ocorre quando os fótons de luz são absorvidos pelo material, causando a geração de corrente elétrica.
            Painéis solares, compostos por muitas células fotovoltaicas, coletam luz solar e a convertem em energia elétrica. Essa energia pode então ser usada diretamente ou armazenada em baterias para uso posterior, fornecendo uma fonte de energia renovável e sustentável com impacto ambiental mínimo.
            Exemplo de input: 
            Quais são os princípios por trás da geração de energia solar?
            Exemplo de input reescrito:
            Como as células fotovoltaicas funcionam para converter a luz solar em energia elétrica, e qual é o papel dos painéis solares nesse processo, incluindo o armazenamento de energia para uso sustentável?
            **

            Input:
            {input}
            Contexto:
            {context}
            Input Reescrito:
            """
        )

    @staticmethod
    def constrained_evolution(input, context):
        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. Reescreva o `Input` adicionando pelo menos uma restrição ou requisito adicional.
            2. O `Input` reescrito deve ser completamente respondível a partir das informações no `Contexto`.
            5. O `Input` reescrito não deve conter mais do que 15 palavras. Use abreviações sempre que possível.

            **
            EXEMPLOS
            Exemplo de contexto:
            As florestas tropicais abrigam mais da metade das espécies de plantas e animais do mundo, tornando-as essenciais para a manutenção da biodiversidade global. A variedade de vida encontrada nesses ecossistemas contribui para a diversidade genética, que é crucial para a adaptação e sobrevivência em meio a condições ambientais em mudança. Essa biodiversidade também apoia a resiliência dos ecossistemas, permitindo que as florestas se recuperem de perturbações.
            A biodiversidade das florestas tropicais desempenha um papel significativo no bem-estar humano, fornecendo serviços essenciais como purificação do ar e da água, controle de doenças e polinização de culturas. Além disso, muitos medicamentos são derivados de plantas de florestas tropicais, destacando a importância desses ecossistemas para a pesquisa médica e a saúde.
            Exemplo de input: 
            Por que a biodiversidade das florestas tropicais é importante?
            Exemplo de input reescrito:
            Como a biodiversidade das florestas tropicais contribui para a resiliência e recuperação dos ecossistemas diante das perturbações, e de que maneiras ela impacta o bem-estar humano através de serviços como purificação do ar e da água, controle de doenças e polinização de culturas?

            --------------------------

            Exemplo de contexto:
            As abelhas desempenham um papel crítico na polinização de plantas com flores, incluindo muitas frutas e vegetais, contribuindo para a diversidade da vida vegetal e a produção de culturas. Sua atividade apoia o crescimento de árvores, flores e outras plantas, que servem de alimento e abrigo para inúmeros animais, mantendo assim o equilíbrio do ecossistema.
            Além do impacto nas culturas alimentares, as abelhas contribuem para o crescimento de plantas silvestres ao polinizar uma ampla gama de plantas fora de ambientes agrícolas. Essa polinização é vital para a reprodução de muitas plantas, afetando a saúde e sustentabilidade de ecossistemas inteiros.
            Exemplo de input: 
            Qual é o papel das abelhas nos ecossistemas?
            Exemplo de input reescrito:
            Considerando o papel crucial das abelhas na polinização tanto de culturas agrícolas quanto de plantas silvestres, contribuindo assim para a diversidade da vida vegetal e apoiando a base das cadeias alimentares, analise como as abelhas influenciam o crescimento e a sustentabilidade de vários ecossistemas.

            --------------------------

            Exemplo de contexto:
            A geração de energia solar depende de células fotovoltaicas para converter a luz solar em eletricidade. Essas células são feitas de materiais que apresentam o efeito fotovoltaico, que ocorre quando fótons de luz são absorvidos pelo material, causando a geração de corrente elétrica.
            Painéis solares, compostos por muitas células fotovoltaicas, coletam luz solar e a convertem em energia elétrica. Essa energia pode então ser usada diretamente ou armazenada em baterias para uso posterior, proporcionando uma fonte de energia renovável e sustentável com impacto ambiental mínimo.
            Exemplo de input: 
            Quais são os princípios por trás da geração de energia solar?
            Exemplo de input reescrito:
            Examine a importância da biodiversidade das florestas tropicais na sustentação da resiliência dos ecossistemas e no fornecimento de serviços essenciais como controle de doenças e polinização de culturas, ao lado de seu papel crucial na pesquisa médica e no desenvolvimento de novos medicamentos. Considere as implicações mais amplas da perda de biodiversidade no equilíbrio ecológico global e na saúde humana.
            **

            Contexto:
            {context}
            Input:
            {input}
            Input Reescrito:
            """
        )

    @staticmethod
    def comparative_question_evolution(input, context):
        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. Reescreva `Input` para focar na comparação de duas ou mais entidades, conceitos ou processos.
            2. `Input` Reescrito deve encorajar uma comparação detalhada que destaque similaridades e diferenças.
            3. `Input` Reescrito deve ser completamente respondível a partir das informações no `Contexto`.
            4. `Input` Reescrito deve ser conciso e compreensível por humanos.
            5. `Input` Reescrito não deve conter frases como 'com base no contexto fornecido' ou 'de acordo com o contexto'.
            6. `Input` Reescrito não deve conter mais de 15 palavras. Use abreviações sempre que possível.

            **
            EXEMPLOS
            Exemplo de contexto:
            "A água entra em ebulição a 100°C (212°F) ao nível do mar, mas o ponto de ebulição diminui com a altitude devido à menor pressão atmosférica. Em contraste, o álcool entra em ebulição a cerca de 78°C (172°F)."
            Exemplo de input: 
            O que acontece com a água quando ela entra em ebulição?
            Exemplo de input reescrito:
            Como o ponto de ebulição da água ao nível do mar se compara ao do álcool, e como a altitude afeta o ponto de ebulição da água?

            --------------------------

            Exemplo de contexto:
            "A fotossíntese nas plantas envolve a conversão de dióxido de carbono e água em glicose e oxigênio, usando a luz solar. A respiração celular nos animais converte glicose e oxigênio de volta em dióxido de carbono e água, liberando energia."
            Exemplo de input: 
            Como as plantas e animais processam energia?
            Exemplo de input reescrito:
            Compare os processos de fotossíntese nas plantas e respiração celular nos animais, focando nas entradas e saídas de cada processo.

            --------------------------

            Exemplo de contexto:
            "O Renascimento foi um período de significativo renascimento cultural, artístico e científico que começou no século 14, principalmente na Itália. O Iluminismo, ocorrendo principalmente no século 18, centrou-se na razão, ciência e individualismo, influenciando significativamente o pensamento europeu."
            Exemplo de input: 
            O que foi o Renascimento?
            Exemplo de input reescrito:
            Contraste os principais focos e impactos do Renascimento e do Iluminismo no pensamento e cultura europeus.

            --------------------------

            Contexto:
            {context}
            Input:
            {input}
            Input Reescrito:
            """
        )

    @staticmethod
    def hypothetical_scenario_evolution(input, context):
        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. Reescreva `Input` para incluir um cenário hipotético ou especulativo que seja relevante para o `Contexto`.
            2. O `Input` reescrito deve encorajar o leitor a aplicar conhecimentos do `Contexto` para imaginar ou deduzir resultados.
            3. O `Input` reescrito deve ser conciso, claro e compreensível por humanos.
            4. O `Input` reescrito não deve conter frases como 'com base no contexto fornecido' ou 'de acordo com o contexto'.
            5. O `Input` reescrito deve ser completamente respondível a partir das informações no `Contexto`.
            6. O `Input` reescrito não deve conter mais de 15 palavras. Use abreviações sempre que possível.

            **
            EXEMPLOS

            Exemplo de contexto:
            O efeito estufa é um processo natural onde a atmosfera da Terra retém parte da energia do Sol, aquecendo o planeta a uma temperatura que suporta a vida. As atividades humanas, especialmente a emissão de gases de efeito estufa como dióxido de carbono e metano, intensificaram esse efeito, levando ao aquecimento global e às mudanças climáticas.
            Exemplo de input:
            Quais são as consequências do efeito estufa?
            Exemplo de input reescrito:
            Imagine um mundo onde as emissões de gases de efeito estufa foram duplicadas da noite para o dia. Como esse efeito estufa intensificado poderia impactar os padrões climáticos globais e os ecossistemas?

            --------------------------

            Exemplo de contexto:
            Antibióticos são medicamentos usados para tratar infecções bacterianas. Eles funcionam matando bactérias ou impedindo seu crescimento. No entanto, o uso excessivo e inadequado de antibióticos levaram ao desenvolvimento de bactérias resistentes a antibióticos, que são mais difíceis de tratar porque podem resistir aos medicamentos projetados para matá-las.
            Exemplo de input:
            Como os antibióticos funcionam?
            Exemplo de input reescrito:
            Em um cenário onde um novo superbug resistente a antibióticos emerge, como os princípios de ação e resistência a antibióticos influenciariam nossa abordagem ao tratamento?

            --------------------------

            Exemplo de contexto:
            A computação quântica se baseia nos princípios da mecânica quântica para processar informações, utilizando bits quânticos ou qubits. Esses qubits podem existir em múltiplos estados simultaneamente, permitindo que os computadores quânticos realizem cálculos complexos muito mais rapidamente do que os computadores tradicionais.
            Exemplo de input:
            O que é computação quântica?
            Exemplo de input reescrito:
            Suponha que um computador quântico tenha sido encarregado de resolver um problema que atualmente levaria séculos para ser resolvido por computadores tradicionais. Como as capacidades únicas da computação quântica poderiam alterar o resultado?
            **

            Contexto:
            {context}
            Input:
            {input}
            Input Reescrito:
            """
        )

    @staticmethod
    def in_breadth_evolution(input, context):
        return (
            EvolutionTemplate.base_instruction
            + f"""
            1. Reescreva `Input` para criar um novo prompt.
            2. `Rewritten Input` deve pertencer ao mesmo domínio que o `input`, mas ser ainda mais raro.
            3. `Rewritten Input` deve ser conciso, claro e compreensível por humanos.
            4. `Rewritten Input` não deve conter frases como 'com base no contexto fornecido' ou 'de acordo com o contexto'.
            5. `Rewritten Input` não deve conter mais do que 15 palavras. Use abreviações sempre que possível.

            **
            EXEMPLOS

            Exemplo de contexto:
            A tecnologia vestível revolucionou o monitoramento da saúde pessoal, permitindo que indivíduos acompanhem os sinais vitais e os níveis de atividade em tempo real.
            Exemplo de input:
            Explore o impacto da tecnologia vestível na gestão da saúde pessoal.
            Exemplo de rewritten input:
            Aprofunde-se no desenvolvimento de dispositivos de saúde implantáveis e seu potencial para transformar a gestão de doenças crônicas.

            --------------------------

            Exemplo de contexto:
            A computação quântica aproveita os princípios da mecânica quântica para processar informações, oferecendo avanços significativos sobre os métodos de computação tradicionais.
            Exemplo de input:
            Como a computação quântica é diferente da computação tradicional?
            Exemplo de rewritten input:
            Explore o potencial da criptografia quântica na melhoria das medidas de cibersegurança além dos padrões atuais de criptografia.

            --------------------------

            Exemplo de contexto:
            A realidade virtual (RV) oferece experiências de aprendizado imersivas, transformando metodologias educacionais ao fornecer maneiras interativas e envolventes de adquirir conhecimento, especialmente em áreas que exigem habilidades práticas.
            Exemplo de input:
            Qual impacto a realidade virtual (RV) tem na educação?
            Exemplo de rewritten input:
            Investigue o uso de simulações de RV no treinamento médico para aprimorar habilidades práticas e tomada de decisões sob pressão.
            **

            Contexto:
            {context}
            Input:
            {input}
            Rewritten Input:
            """
        )
