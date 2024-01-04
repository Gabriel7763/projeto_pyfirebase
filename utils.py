import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import exceptions


def conectar():
    """
    Função para conectar ao servidor
    """
    cred_obj = credentials.Certificate("path/to/serviceAccountKey.json")
    firebase_admin.initialize_app(cred_obj)

    db = firestore.client()
    return db


def listar_usuarios():
    """
    Função para listar os produtos
    """
    db = conectar()

    if db:
        usuarios = db.collection("usuarios").get()
        # se existir usuário
        if usuarios:
            print('Listando usuários...')
            print('--------------------')
            for usuario in usuarios:
                print(f'ID: {usuario.id}')
                print(f"Nome: {usuario.get('nome')}")
                print(f"Email: {usuario.get('email')}")
                print('---------------------')
        else:
            print('Não existem usuários cadastrados')
    else:
        print('Não foi possível conectar com o sevidor')


def criar_usuario():
    """
    Função para inserir um produto
    """
    db = conectar()

    if db:
        nome = input('Informe o nome do usuário: ')
        email = input('Informe o email do usuário: ')

        try:
            usuario = db.collection('usuarios').add(
                {"nome": nome, "email": email})

            if usuario:
                print(f'O usuário {nome} foi inserido com sucesso!')
            else:
                print('Não foi possível criar o usuário')
        except exceptions.FirebaseError as e:
            print(f'Não foi possível criar o usuário: {e}')
    else:
        print('Não foi possível conectar com o sevidor')


def atualizar_usuario():
    """
    Função para atualizar um produto
    """
    db = conectar()

    if db:
        id_usuario = input('Informe o id do usuário: ')
        # validando existencia do usuário
        documento = db.collection('usuarios').document(id_usuario).get()
        if not documento.exists:
            print('Usuário não existe')
        else:
            nome = input('Informe o nome do usuário: ')
            email = input('Informe o email do usuário: ')

            novos_dados = ({'nome': nome, 'email': email})
            try:
                usuario = db.collection('usuarios').document(id_usuario)
                usuario.update(novos_dados)
                print('Dados do usuário foram atualizados')
            except exceptions.FirebaseError as e:
                print(f'Não foi possível atualizar o usuário: {e}')
    else:
        print('Não foi possível conectar com o sevidor')


def deletar_usuario():
    """
    Função para deletar um produto
    """
    db = conectar()
    id_usuario = input('Informe o ID do usuário: ')

    if db:
        try:
            usuario = db.collection('usuarios').document(id_usuario)
            usuario.delete()
            print('Usuário deletado com sucesso!')
        except exceptions.FirebaseError as e:
            print(f'Não foi possível deletar o usuário: {e}')
    else:
        print('Erro ao conectar ao servidor')


def menu():
    """
    Função para gerar o menu inicial
    """
    print('=========Gerenciamento de Produtos==============')
    print('Selecione uma opção: ')
    print('1 - Listar usuários.')
    print('2 - Criar usuário.')
    print('3 - Atualizar usuário.')
    print('4 - Deletar usuário.')
    opcao = int(input())
    if opcao in [1, 2, 3, 4]:
        if opcao == 1:
            listar_usuarios()
        elif opcao == 2:
            criar_usuario()
        elif opcao == 3:
            atualizar_usuario()
        elif opcao == 4:
            deletar_usuario()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
