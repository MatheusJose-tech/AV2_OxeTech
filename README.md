# AV2 OxeTech — Refatoração do Sistema Gilded Rose

Projeto final da disciplina de **Boas Práticas de Desenvolvimento de Software** (curso OxeTech). O trabalho consistiu em pegar o clássico *kata* de refatoração **Gilded Rose** — um sistema de controle de estoque de uma loja medieval — e evoluí-lo de um código difícil de manter para uma arquitetura orientada a objetos, testável e extensível, sem alterar o comportamento externo original.

## Índice

- [Estrutura de pastas](#estrutura-de-pastas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como rodar os testes](#como-rodar-os-testes)
- [O código original (legado)](#o-código-original-legado)
- [Abordagem adotada](#abordagem-adotada)
- [Arquitetura refatorada](#arquitetura-refatorada)
- [Padrões de projeto aplicados](#padrões-de-projeto-aplicados)
- [Princípios de design aplicados](#princípios-de-design-aplicados)
- [Adicionando um novo tipo de item](#adicionando-um-novo-tipo-de-item-exemplo-de-extensibilidade)
- [Regras de negócio por tipo de item](#regras-de-negócio-por-tipo-de-item)
- [Testes](#testes)
- [Autor](#autor)

## Estrutura de pastas

```
AV2_OxeTech/
├── estoque/
│   ├── armazem.py        # Classes de domínio (Produto e subclasses)
│   └── constante.py      # Mapeamento nome do item -> classe (Factory)
├── loja/
│   └── sistema.py        # Classe Loja: orquestra a atualização dos produtos
├── tests/
│   └── test_gilded_rose.py   # Suíte de testes (pytest)
├── glided_rose.py         # Implementação original (legado), mantida como referência
├── requirements.txt
└── README.md
```

## Pré-requisitos

- Python 3.10+
- pip

## Instalação

```bash
git clone https://github.com/MatheusJose-tech/AV2_OxeTech.git
cd AV2_OxeTech
pip install -r requirements.txt
```

## Como rodar os testes

```bash
pytest -v
```

A suíte tem 15 testes, todos passando, cobrindo as regras de negócio de cada tipo de item.

## O código original (legado)

`glided_rose.py` contém a implementação inicial do sistema, recebida pronta como ponto de partida do exercício: uma única classe `GildedRose` com um método `att()` cheio de condicionais aninhados (`if` dentro de `if` dentro de `if`) tratando todas as regras de todos os itens no mesmo lugar. É o "código legado" clássico do kata — funciona, mas é difícil de entender, testar e estender, já que qualquer novo tipo de item exigiria mexer no mesmo bloco de lógica, arriscando quebrar os demais.

Esse arquivo foi mantido no repositório apenas como referência histórica / ponto de partida da refatoração. **O sistema atual não depende mais dele.**

## Abordagem adotada

1. **Testes de caracterização**: antes de tocar no código legado, escrevemos testes que documentam o comportamento já existente, garantindo uma rede de segurança para refatorar sem quebrar nada.
2. **Refatoração incremental**, com um Pull Request por etapa (classes de produto → mapa de produtos → classe `Loja` → ajustes na classe base → testes atualizados).
3. Depois da refatoração, **adicionamos um novo tipo de item** (Conjured Mana Cake) para validar, na prática, que a nova arquitetura é de fato extensível.

## Arquitetura refatorada

- **`Produto`** (`estoque/armazem.py`): classe base; define o contrato `atualizar()` que toda subclasse deve implementar.
- **Subclasses de `Produto`**, uma por regra de negócio:
  - `Normal` — item comum, perde qualidade normalmente
  - `Queijo_envelhecido` — "Aged Brie", ganha qualidade em vez de perder
  - `Sulfuras` — item lendário, nunca muda
  - `Ingressos_de_show` — "Backstage passes", ganha qualidade a taxas crescentes conforme o show se aproxima e zera depois dele
  - `Item_conjurado` — "Conjured", degrada no dobro da taxa de um item normal
- **`estoque/constante.py`**: dicionário `PRODUTOS`, que mapeia o nome do item para a classe responsável por ele — funciona como uma Factory simples.
- **`loja/sistema.py` — `Loja`**: orquestra o estoque.
  - `adicionar_produtos()`: para cada item recebido, consulta o dicionário `PRODUTOS` (usando `Normal` como padrão se o nome não estiver mapeado) e instancia a classe correta.
  - `atualizar_produtos()`: percorre os produtos e chama `atualizar()` em cada um, sem precisar saber qual é o tipo concreto — isso é resolvido por polimorfismo.

## Padrões de projeto aplicados

- **Strategy** (via herança e polimorfismo): cada tipo de item implementa sua própria variação do método `atualizar()`. A `Loja` apenas chama o método, sem nenhum `if/elif` decidindo qual regra aplicar.
- **Factory (simples)**: o dicionário `PRODUTOS` centraliza a decisão de "qual classe instanciar para qual item", isolando essa responsabilidade do resto do sistema.

## Princípios de design aplicados

- **SRP (Responsabilidade Única)**: cada classe tem um único motivo para mudar — as subclasses de `Produto` cuidam da regra de qualidade de um item específico; `Loja` cuida de orquestrar o estoque; `PRODUTOS` cuida só do mapeamento nome → classe.
- **OCP (Aberto/Fechado)**: para adicionar um novo tipo de item (o Conjured), não foi necessário alterar nenhuma classe existente — só criar uma nova subclasse de `Produto` e registrá-la no dicionário `PRODUTOS`. O sistema está aberto para extensão e fechado para modificação.
- **LSP (Substituição de Liskov)**: qualquer subclasse de `Produto` pode ser usada no lugar da classe base sem quebrar o comportamento da `Loja`, já que todas respeitam o mesmo contrato (`atualizar()`).
- **DRY (Don't Repeat Yourself)**: a lógica de "travar" a qualidade entre 0 e 50 (`min(50, max(0, ...))`) e a atualização de `dias_vendas` ficam isoladas dentro de cada classe, em vez de repetidas em vários `if` espalhados como no código original.
- **KISS (Keep It Simple)**: cada classe resolve uma regra pequena e direta; não há condicionais aninhados — a leitura de qualquer subclasse é linear, de cima para baixo.

## Adicionando um novo tipo de item (exemplo de extensibilidade)

Para demonstrar o OCP na prática, o item **Conjured Mana Cake** foi adicionado ao sistema. Bastou criar a subclasse:

```python
class Item_conjurado(Produto):
    def atualizar(self):
        self.dias_vendas -= 1

        perca_qualidade = 4 if self.dias_vendas < 0 else 2
        nova_qualidade = self.qualidade - perca_qualidade

        self.qualidade = min(50, max(0, nova_qualidade))
```

E registrá-la em `estoque/constante.py`:

```python
PRODUTOS = {
    "Aged Brie": Queijo_envelhecido,
    "Sulfuras, Hand of Ragnaros": Sulfuras,
    "Backstage passes to a TAFKAL80ETC concert": Ingressos_de_show,
    "Conjured Mana Cake": Item_conjurado,
}
```

Nenhuma classe existente precisou ser alterada.

## Regras de negócio por tipo de item

| Item | Comportamento da qualidade | Limite |
|---|---|---|
| Item comum (Normal) | -1 por dia; -2 após vencido (`dias_vendas < 0`) | 0 a 50 |
| Aged Brie | +1 por dia; +2 após vencido | 0 a 50 |
| Sulfuras, Hand of Ragnaros | Não muda; qualidade fixa em 80 | — |
| Backstage passes | +1 (mais de 10 dias); +2 (6 a 10 dias); +3 (1 a 5 dias); cai a 0 após o show | 0 a 50 |
| Conjured Mana Cake | -2 por dia; -4 após vencido (o dobro de um item normal) | 0 a 50 |

## Testes

A suíte em `tests/test_gilded_rose.py` cobre, com `pytest`:

- Degradação normal e acelerada (pós-vencimento) de um item comum
- Valorização normal e acelerada do Aged Brie, sem ultrapassar 50
- Imutabilidade do Sulfuras
- As quatro faixas de qualidade dos Backstage passes (mais de 10, 10, 5 e 0 dias, e vencido), sem ultrapassar 50
- Degradação acelerada do item Conjured
- Limites de qualidade (não fica negativa, não ultrapassa 50)

## Autores

Matheus José, Antônio Carlos e Carlos Henrique — Projeto final da disciplina de Boas Práticas de Desenvolvimento de Software (OxeTech).