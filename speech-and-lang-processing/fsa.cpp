#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <utility>

/* 
   My implementations of Deterministic and Non-Desterministic Finate State Automata as described
   in Daniel Jurafsky's Book, Speech and Language Processing.
 */


using namespace std;

// Each state is a list of transitions -- ordered pairs of (some input type, target state)
template <typename T>
using transition = pair<T, void*>;

template <typename T>
using state = vector<transition<T>>;


template <typename T>
bool ND_FSA_Recognizer(vector<T> tape, state<T> initial_state, const T EPSILON) {
	// Keeps track of available state/index combos
	vector< pair<state<T>*, int> > agenda;

	// Start at the first char of the tape at the first state
	agenda.push_back(pair<state<T>*,int>(&initial_state, 0));
	while (!agenda.empty()) {
		// Get the next state
		pair<state<T>*, int> current = agenda.back();
		agenda.pop_back();
		int current_index = current.second;

		// If we have a null state pointer, we reached an accepting state
		if (current.first == NULL) {
			// Return true if we've reached the end of our input
			if (current_index == tape.size()) return true;
			
			// Otherwise we've reached a dead end
			continue;
		}

		state<T> current_node = *current.first;

		// If there's chars left in the tape
		if (current_index < tape.size()) {
			T input = tape[current_index];

			// Add all possible cbar transition states to the agenda
			for (int i = 0; i < current_node.size(); i++) {
				if (current_node[i].first == input) {
					agenda.push_back(pair<state<T>*, int>((state<T>*)current_node[i].second, current_index+1));
				}
			}
		}

		// Check for empty transitions
		for (int i = 0; i < current_node.size(); i++) {
			if (current_node[i].first == EPSILON) {
				agenda.push_back(pair<state<T>*, int>((state<T>*)current_node[i].second, current_index));
			}
		}
	}
	return false;
}

template <typename T>
bool is_accepting_state(state<T> search_state, const T EPSILON) {
	for (int i = 0; i < search_state.size(); i++) {
		if (search_state[i].first == EPSILON && search_state[i].second == NULL)
			return true;
	}
	return false;
}

template <typename T>
bool D_FSA_Recognizer(string tape, state<T> initial_state, const T EPSILON) {
	int index = 0;
	state<T> current_state = initial_state;

	// While we still have more input
	while (index < tape.size()) {

		char input = tape[index];
		bool found_transition = false;
		// See it there's a valid transistion
		for (int i = 0; i < current_state.size(); i++) {
			if (current_state[i].first == input) {
				current_state = *(state<T>*)(current_state[i].second);
				index++;
				found_transition = true;
				break;
			}
		}
		// Otherwise the pattern doesn't match
		if (!found_transition) {
			return false;
		}

	}
	// If the final state is an accepting state, return true
	// Otherwise return false
	return is_accepting_state<T>(current_state, EPSILON);
}

void sheep_language() {
	const char EPSILON = 0;
	state<char> q0, q1, q2, q3, q4;

	q0.push_back(transition<char>('b', &q1));
	q1.push_back(transition<char>('a', &q2));
	q2.push_back(transition<char>('a', &q3));
	q3.push_back(transition<char>('a', &q3));
	q3.push_back(transition<char>('!', &q4));
	q4.push_back(transition<char>(EPSILON, NULL));

	vector<string> test_input;
	test_input.push_back("baaaaaa!");
	test_input.push_back("baa!");
	test_input.push_back("Hello World");
	test_input.push_back("ba!");
	test_input.push_back("baaa");

	for (int i = 0; i < test_input.size(); i++) {
		vector<char> formatted;
		for (int j = 0; j < test_input[i].size(); j++) {
			formatted.push_back(test_input[i][j]);
		}

		if (ND_FSA_Recognizer(formatted, q0, EPSILON) == true)
			cout << "The string <" << test_input[i] << "> was accepted by the FSA" << endl;
		else
			cout << "The string <" << test_input[i] << "> was not recognized by the FSA" << endl;
	}

}

// Detects dates where the day of the month is 1-5 or 20-25
void date_recognizer() {

	const string EPSILON = "EPSILON";
	state<string> q0, q1, q2, q3;

	q0.push_back(transition<string>("January", &q1));
	q0.push_back(transition<string>("Febuary", &q1));
	q0.push_back(transition<string>("March", &q1));
	q0.push_back(transition<string>("April", &q1));
	q0.push_back(transition<string>("May", &q1));
	q0.push_back(transition<string>("June", &q1));
	q0.push_back(transition<string>("July", &q1));
	q0.push_back(transition<string>("August", &q1));
	q0.push_back(transition<string>("September", &q1));
	q0.push_back(transition<string>("October", &q1));
	q0.push_back(transition<string>("November", &q1));
	q0.push_back(transition<string>("December", &q1));

	q1.push_back(transition<string>("first", &q3));
	q1.push_back(transition<string>("second", &q3));
	q1.push_back(transition<string>("third", &q3));
	q1.push_back(transition<string>("fourth", &q3));
	q1.push_back(transition<string>("fifth", &q3));
	
	q1.push_back(transition<string>("twenty", &q2));
	
	q2.push_back(transition<string>("first", &q3));
	q2.push_back(transition<string>("second", &q3));
	q2.push_back(transition<string>("third", &q3));
	q2.push_back(transition<string>("fourth", &q3));
	q2.push_back(transition<string>("fifth", &q3));

	q3.push_back(transition<string>(EPSILON, NULL));

	vector<string> test_input;
	test_input.push_back("January fourth");
	test_input.push_back("March first");
	test_input.push_back("May fourth twenty");
	test_input.push_back("December twenty third");
	test_input.push_back("asdfasdf");

	for (int i = 0; i < test_input.size(); i++) {
		vector<string> formatted;
	   	stringstream s(test_input[i]);
	   	while(!s.eof()) {
	   	   	string tmp;
	   	   	s >> tmp;
	   	   	formatted.push_back(tmp);
		}

		if (ND_FSA_Recognizer<string>(formatted, q0, EPSILON) == true)
				cout << "The string <" << test_input[i] << "> was accepted by the FSA" << endl;
			else
				cout << "The string <" << test_input[i] << "> was not recognized by the FSA" << endl;
	}

}


int main(int argc, char ** argv) {
	cout << "Recognizing sheep language: /baa+!/" << endl << endl;
	sheep_language();

	cout << endl << "Recognizing some dates: " << endl << endl;
	date_recognizer();

	return 0;
}