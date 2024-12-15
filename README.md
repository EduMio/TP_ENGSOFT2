# Sistema de Atendimento Online para Tratamento Cardiológico

## Desenvolvedores:
- **Eduardo Diniz Mio**
- **Etelvina Costa Santos Sá Oliveira**

## Descrição do Sistema

O sistema é uma aplicação web voltada para o atendimento online e tratamento cardiológico, com funcionalidades específicas para médicos. Entre suas principais funcionalidades estão:

1. **Fila de Urgência**: Gerenciamento e priorização dos pacientes de acordo com a gravidade de seus casos.
2. **Cadastro de Pacientes**: Registro de pacientes na plataforma, permitindo acompanhamento contínuo.
3. **Laudo de Exames ECG**: Possibilidade de médicos analisarem e emitirem laudos de exames de eletrocardiograma (ECG).
4. **Visualização de Dados**: Consulta a históricos e informações relevantes sobre os exames e os pacientes.
5. **Laudo Adicional**: Ferramenta para laudar outros parâmetros e dados adicionais do ECG, contribuindo para um diagnóstico mais preciso.

## Tecnologias Utilizadas

1. **Python (Django)**: 
   - Django foi escolhido por ser um framework robusto e seguro para o desenvolvimento web. Ele oferece recursos para construção rápida de sistemas complexos, além de ser altamente escalável.
   - Python é utilizado pela sua simplicidade e eficiência na manipulação de dados médicos.

2. **SQLite**: 
   - Um banco de dados leve e eficiente, ideal para projetos de médio porte. Ele permite um gerenciamento simples e rápido dos dados relacionados aos pacientes e exames.

3. **HTML e CSS**:
   - **HTML**: Utilizado para estruturar as páginas do sistema, garantindo uma interface organizada.
   - **CSS**: Responsável pela estilização e criação de uma interface amigável e acessível para os médicos.

## Como Executar o Sistema

1. Clone este repositório
2. Instale as dependências necessárias: pip install -r requirements.txt
3. Execute as migrações do banco de dados: python manage.py migrate
4. Inicie o servidor: python manage.py runserver
5. Acesse o sistema no navegador pelo endereço: http://127.0.0.1:8000/
6. Rode os testes com o comando: python manage.py test



