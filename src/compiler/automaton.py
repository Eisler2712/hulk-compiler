from queue import Queue
from typing import Dict, Set, List, Tuple
import json

class State:
    def __init__(self, index : int, finished=False) -> None:
        self.index = index
        self.finished: bool = finished
        self.transitions: Dict[str,State] = {}
        self.epsilon_transitions: Set['State'] = set()
        self.complement: State|None = None

    def add_transition(self, symbol: str, state: 'State') -> None:
        self.transitions[symbol] = state

    def add_epsilon_transition(self, state: 'State') -> None:
        self.epsilon_transitions.add(state)

    def goTo(self, symbol:str) -> 'State | None':
        if symbol not in self.transitions:
            return self.transitions[symbol]
        return self.complement

    def goToEpsilon_transition(self) -> List['State']:
        return [s for s in self.epsilon_transitions]

    def toJson(self):
        result = {}

        for k,v in self.transitions.items():
            if not k in result:
                result[k] = []
            result[k].append(v.index)

        result["epsilon_transitions"] = []

        for v in self.epsilon_transitions:
            result["epsilon_transitions"].append(v.index)

        if self.complement is not None:
            result["default"] = self.complement.index

        result['finished'] = self.finished


class Automaton:
    def __init__(self, isCopy=False) -> None:
        self.initState: State = None if isCopy else State(0)

        self.states: List[State] = []if isCopy else [self.initState]


    def add_transition(self, fromState: State, symbol: str, toState: State) -> None:
        fromState.add_transition(symbol,toState)

    def add_epsilon_transition(self,fromState: State, toState: State) -> None:
        fromState.add_epsilon_transition(toState)

    def add_final_state(self,state: State) -> None:
        state.finished = True

    def add_complement(self,fromState: State, toState: State) -> None:
        fromState.complement = toState

    def get_new_state(self, state=None) -> State:
        newState = state if state is not None else State(
            len(self.states))
        newState.index = len(self.states)

        self.states.append(newState)
        return newState

    @property
    def final_states(self) -> List[State]:
        return [state for state in self.states if state.finished]

    def match(self, string: str) -> bool:
        visited = set([])
        return self.__match(self.initState, string, 0, visited)

    def __match(self, state: State, string: str, index, visited: Set[Tuple[int, int]]) -> bool:
        if (state.index, index) in visited:
            return False

        visited.add((state.index, index))

        if index == len(string):
            return state.finished

        for epsilon_state in state.epsilon_transitions:
            if self.__match(epsilon_state, string, index, visited):
                return True

        goTo = state.goTo(string[index])

        if goTo is not None:
            return self.__match(goTo, string, index+1, visited)

        return False

    def join(self, automaton: 'Automaton') -> 'Automaton':
        automaton = automaton.copy()
        self.add_epsilon_transition(self.initState, automaton.initState)

        for state in automaton.states:
            self.get_new_state(state)

        return self

    def concat(self, automaton: 'Automaton') -> 'Automaton':
        automaton = automaton.copy()
        for state in self.final_states:
            self.add_epsilon_transition(state, automaton.initState)
            state.is_final = False

        for state in automaton.states:
            self.get_new_state(state)

        return self

    def many(self) -> 'Automaton':
        for state in self.final_states:
            self.add_epsilon_transition(state, self.initState)

        self.initState.is_final = True

        return self

    def copy(self) -> 'Automaton':
        newAutomaton = Automaton(True)

        for _ in range(len(self.states)):
            newAutomaton.get_new_state()

        newAutomaton.initState = newAutomaton.states[self.initState.index]

        for state in self.states:
            for epsilon_state in state.epsilon_transitions:
                newAutomaton.add_epsilon_transition(
                    newAutomaton.states[state.index], newAutomaton.states[epsilon_state.index])

            for symbol, symbol_state in state.transitions.items():
                newAutomaton.add_transition(
                    newAutomaton.states[state.index], symbol, newAutomaton.states[symbol_state.index])

            newAutomaton.states[state.index].finished = state.finished
            newAutomaton.states[state.index].complement = None if state.complement is None else newAutomaton.states[
                state.complement.index]

        return newAutomaton

    def to_dfa(self) -> 'Automaton':
        newAutomaton = Automaton()
        newNodes: List[Tuple[State, Set[State]]] = []

        initial = set([self.initState])
        self.__goTo_epsilon(initial)
        newNodes.append((newAutomaton.initState, initial))

        newAutomaton.initState.finished = any(
            state for state in initial if state.finished)

        q: Queue[Tuple[Automaton, Set[State]]] = Queue()
        q.put(newNodes[0])

        while not q.empty():
            node, states = q.get()

            symbols = set([])
            for state in states:
                for s in state.transitions:
                    symbols.add(s)

            for symbol in symbols:
                goTo = self.__goTo_symbol(states, symbol)

                self.__next_goTo(goTo, newAutomaton, node,
                                 newNodes, q, symbol)

            goTo = self.__goTo_complement(states)
            self.__next_goTo(goTo, newAutomaton, node, newNodes, q)

        return newAutomaton

    def __next_goTo(self, goTo: Set[State], newAutomaton: 'Automaton', node: 'State', newNodes: List[Tuple[State, Set[State]]], q: Queue, symbol: str | None = None):
        if len(goTo) == 0:
            return

        newNode = self.__get_node(newNodes, goTo)

        if newNode is None:
            newNode = newAutomaton.get_new_state()

            if any(state.finished for state in goTo):
                newAutomaton.add_final_state(newNode)

            newNodes.append((newNode, goTo))
            q.put((newNode, goTo))

        if symbol is not None:
            newAutomaton.add_transition(node, symbol, newNode)
        else:
            newAutomaton.add_complement(node, newNode)

    def __get_node(self, nodes: List[Tuple[State, Set[State]]], states: Set[State]) -> State | None:
        for node, node_states in nodes:
            if all(state in node_states for state in states) and len(node_states) == len(states):
                return node

        return None

    def __goTo_complement(self, states: Set[State]) -> Set[State]:
        goTo = set([])

        for state in states:
            if state.complement is None:
                continue

            goTo.add(state.complement)

        self.__goTo_epsilon(goTo)

        return goTo

    def __goTo_epsilon(self, states: Set[State]):
        change = True

        while change:
            change = False
            aux = []

            for state in states:
                for epsilon_state in state.goToEpsilon_transition():
                    if epsilon_state not in states:
                        aux.append(epsilon_state)

            for state in aux:
                change = True
                states.add(state)

    def __goTo_symbol(self, states: Set[State], symbol: str) -> Set[State]:
        goTo = set()

        for state in states:
            symbol_state = state.goTo(symbol)
            if symbol_state is None:
                continue
            goTo.add(symbol_state)

        self.__goTo_epsilon(goTo)

        return goTo

    def load(self, name: str):
        cache = json.load(open(f"cache/{name}_automaton.json"))
        self.from_json(cache)

    def build(self, name: str):
        cache = self.to_json()
        json.dump(cache, open(f"cache/{name}_automaton.json", 'w'))

    def to_json(self):
        result = []

        for v in self.states:
            result.append(v.toJson())

        return result

    def from_json(self, jsonDict):
        self.states.clear()

        for _ in range(len(jsonDict)):
            self.get_new_state()

        for i, s in enumerate(jsonDict):
            for k, v in s.items():
                if k == "eok":
                    for n in v:
                        self.states[i].add_epsilon_transition(self.states[n])
                    continue

                if k == "default":
                    self.states[i].complement = self.states[v]
                    continue

                if k == 'is_final':
                    self.states[i].finished = v
                    continue

                for n in v:
                    self.states[i].add_transition(self.states[n])

        self.initState = self.states[0]


def pattern_to_automaton(pattern: str) -> Automaton:
    automaton = Automaton()

    state = automaton.initState

    for symbol in pattern:
        newState = automaton.get_new_state()
        automaton.add_transition(state, symbol, newState)
        state = newState

    automaton.add_final_state(state)

    return automaton



