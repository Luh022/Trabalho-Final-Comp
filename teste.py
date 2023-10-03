class Node:     #Criação da classe Nó
    def __init__(item, num):    
        item.num = num      #'num' é o valor que o nó armazena
        item.tamanho = 3    #Altura da árvore a partir do nó    
        item.esquerda = None        #Ponteiro para os nós filhos da esquerda
        item.direita = None         #Ponteiro para os nós filhos da direita


class AVLTree:      #Criação da árvore binária
    def _tamanho(item, node):       #Função da altura da árvore
        if node is None:        #Condição para o valor do atributo 'node', caso seja nulo
            return 0
        return node.tamanho     #Retorna o valor da altura da árvore a partir do nó se o 'node' não for nulo

    def _balancear_factor(item, node):      #Função do 'fator de balanceamento'
        if node is None:         #Condição para o valor do atributo 'node', caso seja nulo
            return 0
        return item._tamanho(node.esquerda) - item._tamanho(node.direita)   #Calculo a diferença das alturas das subárvores esquerda e direita se o 'node' não for nulo 

    def _fix_tamanho(item, node):       #Faz parte das Rotações Simples
        node.tamanho = 1 + max(item._tamanho(node.esquerda), item._tamanho(node.direita))   #Operação para calcular a altura dos nós movimentados nas operações

    def _rotacionar_esquerda(item, x):      #Implementação de Rotação Simples à Esquerda
        y = x.direita           #Nó raíz se torna filho à esquerda do nó que era seu filho à direita
        x.direita = y.esquerda      #O nó filho à direita do nó raíz passa a ser o filho que estava à esquerda
        y.esquerda = x
        item._fix_tamanho(x)        #Chamando a função '_fix_tamanho',
        item._fix_tamanho(y)        #Responsável por recalcular a altura dos nós que foram movimentados
        return y

    def _rotacionar_direita(item, y):       #Implementação de Rotação Simples à Direita
        x = y.esquerda          #Nó raíz se torna filho à direita do nó que era seu filho à esquerda
        y.esquerda = x.direita      #O nó filho à esquerda do nó raíz passa a ser o filho que estava à direita
        x.direita = y
        item._fix_tamanho(y)        #Chamando a função '_fix_tamanho',
        item._fix_tamanho(x)        #Responsável por recalcular a altura dos nós que foram movimentados
        return x

    def _balancear(item, node):     #Código para balanceamento da árvore
        item._fix_tamanho(node)     
        balancear = item._balancear_factor(node)    #Verificar o fator de balanceamento

        if balancear > 1:       #Condição de desequilíbrio caso o fator de balanceamento de um nó for maior que 1
            if item._balancear_factor(node.esquerda) < 0:       #Condição se houver desbalanceamento causado por uma inserção na subárvore direita do filho direito
                node.esquerda = item._rotacionar_esquerda(node.esquerda)    #A função 'rotacionar_esquerda' é chamada, o que faz a rotação mover cada nó uma posição para a direita da posição atual
            return item._rotacionar_direita(node)       #Caso o desbalanceamento não seja em uma subárvore direita, mas sim no lado esquerdo, então deve ocorrer uma rotação simples à direita

        if balancear < -1:      #Condição de desequilíbrio caso o fator de balanceamento de um nó for menor que -1
            if item._balancear_factor(node.direita) > 0:        #Condição se houver desbalanceamento causado por uma inserção na subárvore esquerda do filho esquerdo
                node.direita = item._rotacionar_direita(node.direita)   #A função 'rotacionar_direita' é chamada, o que faz a rotação mover cada nó uma posição para a esquerda da posição atual
            return item._rotacionar_esquerda(node)      #Caso o desbalanceamento não seja em uma subárvore esquerda, mas sim no lado direito, então deve ocorrer uma rotação simples à esquerda

        return node

    def inserir(item, root, num):       #Definição da função de inserção
        if root is None:        #Verificação se a árvore está vazia
            return Node(num)    #Caso a condição seja verdadeira, um novo nó é criado
        
        if num < root.num:      #Condição para analisar se o valor a ser inserido é menor que o número da raíz
            root.esquerda = item.inserir(root.esquerda, num)    #Se a condição for verdadeira então o número será inserido na subárvore à esquerda
        else:
            root.direita = item.inserir(root.direita, num)      #Se a condição for falsa então o número será inserido na subárvore à direita
        
        return item._balancear(root)        #Executa a função de balanceamento para garantir que a árvore permaneça equilibrada

    def deletar(item, root, num):       #Definição da função de exclusão
        if root is None:        #Verificação se a árvore está vazia
            return root     #Caso seja verdadeira, apenas retorna nulo

        if num < root.num:      #Condição se o número a ser excluído é menor que o número na raíz
            root.esquerda = item.deletar(root.esquerda, num)    #Se a condição for verdadeira então o número será deletado na subárvore à esquerda
        elif num > root.num:    #Condição se o número a ser excluído é maior que o número na raíz
            root.direita = item.deletar(root.direita, num)      #Se a condição for verdadeira então o número será deletado na subárvore à direita
        else:       #Se o valor a ser deletado é igual ao número da raíz
            if root.esquerda is None:       #Se a subárvore esquerda do nó a ser excluído for nula,
                return root.direita         #A subárvore direita é retornada para conectar ao pai do nó deletado
            elif root.direita is None:      #Se a subárvore direita do nó a ser excluído for nula,
                return root.esquerda        #A subárvore esquerda é retornada para conectar ao pai do nó deletado

        return item._balancear(root)        #Executa a função de balanceamento para garantir que a árvore permaneça equilibrada

    def procurar(item, root, num):      #Definição da função de procura
        if root is None or root.num == num:     #Condição para verificar se a raíz atual é nula ou se o valor na raíz é igual ao número que se está procurando
            return root     #Se qualquer uma das condições for verdadeira, retorna-se apenas a raíz atual

        if num < root.num:      #Condição se o número sendo procurado é menor que o número da raíz
            return item.procurar(root.esquerda, num)        #Caso a condição seja verdadeira, então é executada a função 'procurar' na subárvore à esquerda
        return item.procurar(root.direita, num)     #Se a condição for falsa, então a função 'procurar' é executada na subárvore à direita

    def inorder_traversal(item, root):      #Definição da função utilizada para percorrer os nós da árvore em ordem (in-order)
        if root:        #Verificação se a raíz não é nula
            item.inorder_traversal(root.esquerda)       #Sendo a condição verdadeira, a própria função é executada na subárvore esquerda
            print(root.num, end=" ")        #Impressão do número na raíz
            item.inorder_traversal(root.direita)        #Por fim, a função também é executada na subárvore direita

