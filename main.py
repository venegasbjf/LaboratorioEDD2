# Librerias necesarias 
import pandas as pd
from anytree import Node, RenderTree

# Clase para representar un nodo en el Árbol AVL
class TreeNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

# Función para obtener la altura de un nodo
def get_height(node):
    if node is None:
        return 0
    return node.height

# Función para obtener el factor de equilibrio de un nodo
def get_balance_factor(node):
    if node is None:
        return 0
    return get_height(node.left) - get_height(node.right)

# Clase para representar un Árbol AVL
class AVLTree:
    def __init__(self):
        self.root = None

    # Función para insertar un nodo en el Árbol AVL
    def insert(self, key, data):
        if not self.root:
            self.root = TreeNode(key, data)
        else:
            self.root = self._insert(self.root, key, data)

    # Función auxiliar para la inserción de un nodo
    def _insert(self, node, key, data):
        if not node:
            return TreeNode(key, data)

        if key < node.key:
            node.left = self._insert(node.left, key, data)
        else:
            node.right = self._insert(node.right, key, data)

        node.height = 1 + max(get_height(node.left), get_height(node.right))
        balance = get_balance_factor(node)

        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)

        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)

        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        
        return node
    
    # Función para realizar una rotación a la izquierda en el Árbol AVL
    def rotate_left(self, z):
        if z is None or z.right is None:
            return z

        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(get_height(z.left), get_height(z.right))
        y.height = 1 + max(get_height(y.left), get_height(y.right))

        return y
    
    # Función para realizar una rotación a la derecha en el Árbol AVL
    def rotate_right(self, y):
        if y is None or y.left is None:
            return y

        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(get_height(y.left), get_height(y.right))
        x.height = 1 + max(get_height(x.left), get_height(x.right))

    # Función para insertar un nodo en el Árbol AVL utilizando la métrica
    def insert_property(self, property_data):
        metric1 = property_data['price'] / property_data['surface_total']
        self.root = self._insert_property(self.root, metric1, property_data)

    # Función auxiliar para la inserción de un nodo utilizando la métrica
    def _insert_property(self, node, metric1, property_data):
        if not node:
            return TreeNode(metric1, property_data)

        if metric1 < node.key:
            node.left = self._insert_property(node.left, metric1, property_data)
        elif metric1 > node.key:
            node.right = self._insert_property(node.right, metric1, property_data)
        else:
            metric2 = property_data['price'] / (property_data['surface_total'] + property_data['bedrooms'] + property_data['bathrooms'])
            node.right = self._insert_property(node.right, metric1, property_data)  # Insertar en el subárbol derecho
            node.right = self._insert_property(node.right, metric2, property_data)  # Insertar en el subárbol derecho con metric2

        node.height = 1 + max(get_height(node.left), get_height(node.right))
        balance = get_balance_factor(node)

        if balance > 1 and metric1 < node.left.key:
            return self.rotate_right(node)

        if balance < -1 and metric1 > node.right.key:
            return self.rotate_left(node)

        if balance > 1 and metric1 > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1 and metric1 < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        
        return node
    
    # Función para convertir el Árbol AVL a una estructura de árbol general AnyTree
    def _convert_to_anytree(self, node):
        if node:
            new_node = Node(f"Key: {node.key}, Data: {node.data}")
            children = []

            if node.left:
                children.append(self._convert_to_anytree(node.left))
            if node.right:
                children.append(self._convert_to_anytree(node.right))

            new_node.children = children
            return new_node
        
    # Función para imprimir el Árbol AVL en forma de árbol
    def print_tree(self):
        if self.root is not None:
            anytree_root = self._convert_to_anytree(self.root)
            for pre, fill, node in RenderTree(anytree_root):
                print(f"{pre}{node.name}")

    # Función para eliminar un nodo por métrica
    def delete_node_by_metric(self, metric):
        self.root = self._delete_node_by_metric(self.root, metric)

    # Función auxiliar para la eliminación de un nodo por métrica
    def _delete_node_by_metric(self, node, metric):
        if not node:
            return node

        if metric < node.key:
            node.left = self._delete_node_by_metric(node.left, metric)
        elif metric > node.key:
            node.right = self._delete_node_by_metric(node.right, metric)
        else:
            # Nodo encontrado, proceder con la eliminación
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Si el nodo tiene dos hijos, obtener el sucesor en orden
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.data = temp.data
            node.right = self._delete_node_by_metric(node.right, temp.key)

        # Actualizar la altura y equilibrar el árbol
        node.height = 1 + max(get_height(node.left), get_height(node.right))
        balance = get_balance_factor(node)

        if balance > 1 and get_balance_factor(node.left) >= 0:
            return self.rotate_right(node)

        if balance < -1 and get_balance_factor(node.right) <= 0:
            return self.rotate_left(node)

        if balance > 1 and get_balance_factor(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1 and get_balance_factor(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    # Función para obtener el nodo con el valor mínimo en el Árbol AVL
    def _get_min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    # Función para buscar un nodo por métrica
    def search_node_by_metric(self, metric):
        return self._search_node_by_metric(self.root, metric)

    # Función auxiliar para buscar un nodo por métrica
    def _search_node_by_metric(self, node, metric):
        if not node:
            return None

        if metric < node.key:
            return self._search_node_by_metric(node.left, metric)
        elif metric > node.key:
            return self._search_node_by_metric(node.right, metric)
        else:
            return node.data

    # Función para buscar nodos que cumplan con ciertos criterios
    def search_nodes_by_criteria(self, criteria):
        nodes_found = []
        self._search_nodes_by_criteria(self.root, criteria, nodes_found)
        return nodes_found

    # Función auxiliar para buscar nodos que cumplan con ciertos criterios
    def _search_nodes_by_criteria(self, node, criteria, result):
        if not node:
            return

        if self._meets_criteria(node.data, criteria):
            result.append(node.data)

        if node.key >= criteria['min_metric']:
            self._search_nodes_by_criteria(node.left, criteria, result)
        if node.key < criteria['max_metric']:
            self._search_nodes_by_criteria(node.right, criteria, result)

    # Función para verificar si un nodo cumple con ciertos criterios
    def _meets_criteria(self, data, criteria):
        if criteria['city'] and data['city'] != criteria['city']:
            return False
        if criteria['bedrooms'] and data['bedrooms'] < criteria['bedrooms']:
            return False
        if criteria['price'] and data['price'] > criteria['price']:
            return False
        return True

    # Función para mostrar el menú adicional después de mostrar el recorrido por niveles
    def show_menu_after_level_order(self):
        while True:
            print("\nMenú adicional:")
            print("a. Obtener el nivel del nodo")
            print("b. Obtener el factor de balanceo del nodo")
            print("c. Encontrar el padre del nodo")
            print("d. Encontrar el abuelo del nodo")
            print("e. Encontrar el tío del nodo")
            print("f. Volver al menú principal")

            choice = input("Ingrese su elección: ")

            if choice == "a":
                metric_to_find = float(input("Ingrese la métrica1 del nodo para obtener su nivel: "))
                level = self.get_node_level(metric_to_find)
                if level is not None:
                    print(f"Nivel del nodo con métrica {metric_to_find}: {level}")
                else:
                    print(f"Nodo con métrica {metric_to_find} no encontrado.")
            elif choice == "b":
                metric_to_find = float(input("Ingrese la métrica1 del nodo para obtener su factor de balanceo: "))
                balance_factor = self.get_balance_factor_of_node(metric_to_find)
                if balance_factor is not None:
                    print(f"Factor de balanceo del nodo con métrica {metric_to_find}: {balance_factor}")
                else:
                    print(f"Nodo con métrica {metric_to_find} no encontrado.")
            elif choice == "c":
                metric_to_find = float(input("Ingrese la métrica1 del nodo para encontrar su padre: "))
                parent_data = self.find_parent_of_node(metric_to_find)
                if parent_data is not None:
                    print(f"El padre del nodo con métrica {metric_to_find} es:")
                    print(parent_data)
                else:
                    print(f"Nodo con métrica {metric_to_find} no encontrado.")
            elif choice == "d":
                metric_to_find = float(input("Ingrese la métrica1 del nodo para encontrar su abuelo: "))
                grandparent_data = self.find_grandparent_of_node(metric_to_find)
                if grandparent_data is not None:
                    print(f"El abuelo del nodo con métrica {metric_to_find} es:")
                    print(grandparent_data)
                else:
                    print(f"Nodo con métrica {metric_to_find} no encontrado.")
            elif choice == "e":
                metric_to_find = float(input("Ingrese la métrica1 del nodo para encontrar su tío: "))
                uncle_data = self.find_uncle_of_node(metric_to_find)
                if uncle_data is not None:
                    print(f"El tío del nodo con métrica {metric_to_find} es:")
                    print(uncle_data)
                else:
                    print(f"Nodo con métrica {metric_to_find} no encontrado.")
            elif choice == "f":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    # Función para obtener el nivel de un nodo dado su métrica1
    def get_node_level(self, metric):
        return self._get_node_level(self.root, metric, level=1)

    # Función auxiliar para obtener el nivel de un nodo
    def _get_node_level(self, node, metric, level):
        if not node:
            return None

        if metric == node.key:
            return level
        elif metric < node.key:
            return self._get_node_level(node.left, metric, level + 1)
        else:
            return self._get_node_level(node.right, metric, level + 1)

    # Función para obtener el factor de balanceo de un nodo dado su métrica1
    def get_balance_factor_of_node(self, metric):
        return self._get_balance_factor_of_node(self.root, metric)

    # Función auxiliar para obtener el factor de balanceo de un nodo
    def _get_balance_factor_of_node(self, node, metric):
        if not node:
            return None

        if metric == node.key:
            return get_balance_factor(node)
        elif metric < node.key:
            return self._get_balance_factor_of_node(node.left, metric)
        else:
            return self._get_balance_factor_of_node(node.right, metric)

    # Función para encontrar el padre de un nodo dado su métrica1
    def find_parent_of_node(self, metric):
        return self._find_parent_of_node(self.root, metric)

    # Función auxiliar para encontrar el padre de un nodo
    def _find_parent_of_node(self, node, metric):
        if not node:
            return None

        if (node.left and node.left.key == metric) or (node.right and node.right.key == metric):
            return node.data

        if metric < node.key:
            return self._find_parent_of_node(node.left, metric)
        else:
            return self._find_parent_of_node(node.right, metric)

    # Función para encontrar el abuelo de un nodo dado su métrica1
    def find_grandparent_of_node(self, metric):
        return self._find_grandparent_of_node(self.root, metric)

    # Función auxiliar para encontrar el abuelo de un nodo
    def _find_grandparent_of_node(self, node, metric):
        if not node:
            return None

        if (node.left and node.left.key == metric) or (node.right and node.right.key == metric):
            parent_metric = node.key
            return self.find_parent_of_node(parent_metric)

        if metric < node.key:
            return self._find_grandparent_of_node(node.left, metric)
        else:
            return self._find_grandparent_of_node(node.right, metric)

    # Función para encontrar el tío de un nodo dado su métrica1
    def find_uncle_of_node(self, metric):
        return self._find_uncle_of_node(self.root, metric)

    # Función auxiliar para encontrar el tío de un nodo
    def _find_uncle_of_node(self, node, metric):
        if not node:
            return None

        parent_data = self.find_parent_of_node(metric)
        if parent_data:
            parent_metric = parent_data['price'] / parent_data['surface_total']
            return self.find_sibling_of_node(parent_metric)

        return None

    # Función para encontrar el hermano de un nodo dado su métrica1
    def find_sibling_of_node(self, metric):
        return self._find_sibling_of_node(self.root, metric)

    # Función auxiliar para encontrar el hermano de un nodo
    def _find_sibling_of_node(self, node, metric):
        if not node:
            return None

        if metric == node.key:
            parent_data = self.find_parent_of_node(metric)
            if parent_data:
                parent_metric = parent_data['price'] / parent_data['surface_total']
                if node.key < parent_metric:
                    return parent_data['price'] / parent_data['surface_total']
                else:
                    return self.find_sibling_of_node(parent_metric)
        elif metric < node.key:
            return self._find_sibling_of_node(node.left, metric)
        else:
            return self._find_sibling_of_node(node.right, metric)

# Se carga el dataset desde el archivo CSV
df = pd.read_csv('co_properties_final.csv')

# Se crea una instancia del Árbol AVL
avl_tree = AVLTree()

# Se inserta cada propiedad en el árbol usando la métrica price / surface_total
for index, row in df.iterrows():
    avl_tree.insert_property(row.to_dict())

# Menú principal
while True:
    print("Menú:")
    print("1. Insertar un nodo")
    print("2. Eliminar un nodo por métrica")
    print("3. Buscar un nodo por métrica")
    print("4. Buscar nodos por criterios")
    print("5. Mostrar recorrido por niveles")
    print("6. Salir")

    choice = input("Ingrese su elección: ")

    if choice == "1":
        # Se solicitan los datos necesarios al usuario
        key = float(input("Ingrese la métrica1: "))
        data = {
            'city': input("Ingrese la ciudad: "),
            'bedrooms': int(input("Ingrese el número de dormitorios: ")),
            'price': float(input("Ingrese el precio: ")),
            'surface_total': float(input("Ingrese la superficie total: ")),
            'bathrooms': int(input("Ingrese el número de baños: "))
        }

        # Se Llama la función insert_property
        avl_tree.insert_property({'price': data['price'], 'surface_total': data['surface_total'], 'bedrooms': data['bedrooms'], 'bathrooms': data['bathrooms'], 'city': data['city']})
        
        # Se muestra el árbol actualizado
        avl_tree.print_tree()
        
    elif choice == "2":
        # Se solicita la métrica por la cual desea eliminar el nodo
        metric_to_delete = float(input("Ingrese la métrica1 del nodo que desea eliminar: "))

        # Se implementa la lógica para eliminar el nodo correspondiente
        avl_tree.delete_node_by_metric(metric_to_delete)
        
        # Se muestra el árbol actualizado
        avl_tree.print_tree()

    elif choice == "3":
        # Se solicita la métrica por la cual desea buscar el nodo
        metric_to_find = float(input("Ingrese la métrica1 del nodo que desea buscar: "))

        # Se busca el nodo y se muestra su información si se encuentra
        node_data = avl_tree.search_node_by_metric(metric_to_find)
        if node_data is not None:
            print(f"Nodo encontrado:\n{node_data}")
        else:
            print(f"Nodo con métrica {metric_to_find} no encontrado.")

    elif choice == "4":
        # Se solicitan los criterios de búsqueda al usuario
        criteria = {
            'city': input("Ingrese la ciudad (deje en blanco para cualquier ciudad): "),
            'bedrooms': int(input("Ingrese el número mínimo de dormitorios (deje en blanco para cualquier número): ") or 0),
            'price': float(input("Ingrese el precio máximo (deje en blanco para cualquier precio): ") or float('inf')),
            'min_metric': float(input("Ingrese el valor mínimo de la métrica1 (deje en blanco para cualquier valor): ") or float('-inf')),
            'max_metric': float(input("Ingrese el valor máximo de la métrica1 (deje en blanco para cualquier valor): ") or float('inf'))
        }

        # Se buscan los nodos que cumplan con los criterios y se muestran
        nodes_found = avl_tree.search_nodes_by_criteria(criteria)
        if nodes_found:
            print("Nodos encontrados:")
            for node_data in nodes_found:
                print(node_data)
        else:
            print("No se encontraron nodos que cumplan con los criterios.")

    elif choice == "5":
        # Se muestra el árbol AVL en forma de árbol
        avl_tree.print_tree()
        # Se muestra el menú adicional
        avl_tree.show_menu_after_level_order()

    elif choice == "6":
        break

    else:
        print("Opción no válida. Intente de nuevo.")

