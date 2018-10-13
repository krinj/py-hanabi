package agents;
import hanabAI.*;
import java.util.*;

// ======================================================================================================
// PUBLIC CLASS: Matrix Agent
// ======================================================================================================

public class Agent21789272 implements Agent {

    // Control Constants. This determines agent behaviour.
    private static final float K_NORMAL_PLAY_LIMIT = 0.85f;
    private static final float K_SAFE_PLAY_LIMIT = 1.00f;
    private static final float K_DISCARD_LIMIT = 0.85f;
    private static final float K_HINT_PLAY_BOOST = 1.00f;

    public String toString(){
        return "Prince of Nigeria";
    }

    @Override
    public Action doAction(State state) {
        try {

            // Utility Agent Variables. Good to keep track of.
            int playerIndex = state.getNextPlayer();
            PyState pyState = new PyState(state);
            List<PyCardMatrix> matrices = generateHandMatrix(pyState, playerIndex);

            PyCardMatrix pMatrix = null;  // The Matrix for the most playable card in our hand.
            PyCardMatrix dMatrix = null;  // The Matrix for the most useless card in our hand.
            for (PyCardMatrix m : matrices) {
                pMatrix = (pMatrix == null || pMatrix.getPlayRating() < m.getPlayRating()) ? m : pMatrix;
                dMatrix = (dMatrix == null || dMatrix.getDiscardRating() < m.getDiscardRating()) ? m : dMatrix;
            }

            // Make sure the Matrix is never null.
            assert pMatrix != null;

            // Voluntarily play a card.
            float playLimit = state.getFuseTokens() == 1 ? K_SAFE_PLAY_LIMIT : K_NORMAL_PLAY_LIMIT;
            if (pMatrix.getPlayRating() >= playLimit) {
                return new Action(playerIndex, toString(), ActionType.PLAY, pMatrix.handIndex);
            }

            // Voluntarily discard.
            if (state.getHintTokens() < 8 && dMatrix.getDiscardRating() >= K_DISCARD_LIMIT) {
                return new Action(playerIndex, toString(), ActionType.DISCARD, dMatrix.handIndex);
            }

            // Give hint to another player.
            if (state.getHintTokens() > 0) {
                List<PyHint> hints = getValidHintCommands(pyState, playerIndex);
                PyHint hint = getBestHint(hints);

                // Generate the action for this hint.
                Card[] targetHand = state.getHand(hint.targetIndex);
                boolean[] hintCards = new boolean[targetHand.length];
                for (int i = 0; i < targetHand.length; i++)
                {
                    Card card = targetHand[i];
                    if (card == null)
                        continue;

                    hintCards[i] = false;

                    if (hint.colour != null && hint.colour == card.getColour())
                        hintCards[i] = true;

                    if (hint.value > 0 && hint.value == card.getValue())
                        hintCards[i] = true;
                }

                ActionType hintType = hint.colour == null ? ActionType.HINT_VALUE : ActionType.HINT_COLOUR;
                if (hint.colour == null)
                    return new Action(playerIndex, toString(), hintType, hint.targetIndex, hintCards, hint.value);
                else
                    return new Action(playerIndex, toString(), hintType, hint.targetIndex, hintCards, hint.colour);
            }

            // Forced to discard.
            return new Action(playerIndex, toString(), ActionType.DISCARD, dMatrix.handIndex);

        } catch(IllegalActionException e){
            e.printStackTrace();
            throw new RuntimeException("Something has gone very wrong");
        }
    }

    // ======================================================================================================
    // Analyzer and Matrix Generation Logic.
    // ======================================================================================================

    private List<PyCardMatrix> generateHandMatrix(PyState state, int playerIndex)
    {
        // Generate a PyCardMatrix for each card in hand, based on what we know.
        ArrayList<PyCardMatrix> matrices = new ArrayList<>();
        PyCard[] hand = state.hands[playerIndex];
        Map<String, Integer> observedMap = generateObservationMap(state, playerIndex, -1);

        for (int i = 0; i < hand.length; i++)
        {
            PyCard card = hand[i];
            if (card == null)
                continue;

            // Create a new matrix based on all the information that we know.
            PyCardMatrix matrix = getCardMatrix(
                    state, playerIndex, card.colour, card.value, card.notColour, card.notValue, observedMap);
            matrix.age = card.age;

            // Bind it to this hand.
            matrix.handIndex = i;

            // Favour the hinted cards.
            if (card.hasReceivedValueHint() || card.hasReceivedColourHint())
            {
                if (matrix.getPlayRating() > matrix.getDiscardRating())
                    matrix.playRatingFactor = K_HINT_PLAY_BOOST;
            }

            // Add this to all all known card matrices.
            matrices.add(matrix);
        }
        return matrices;
    }

    private Map<String, Integer> generateObservationMap(PyState state, int playerIndex, int offhandIndex)
    {
        // Use all the information we can see to generate a list of all the possible remaining cards.

        PyCardCounter counter = PyCardCounter.newDeckCounter();

        for (Card card : state.originalState.getDiscards())
            counter.add(card.getColour(), card.getValue(), -1);

        for (Colour colour : Colour.values()) {
            for (Card card : state.originalState.getFirework(colour))
                counter.add(card.getColour(), card.getValue(), -1);
        }

        int numberOfPlayers = state.originalState.getPlayers().length;
        for (int i = 0; i < numberOfPlayers; i++)
        {
            if (i != playerIndex)
            {
                PyCard[] hand = state.hands[i];
                for (PyCard card : hand)
                {
                    if (card == null ||
                            ((offhandIndex == i) && !(card.hasReceivedValueHint() && card.hasReceivedColourHint())))
                        continue;
                    counter.add(card.colour, card.value, -1);
                }
            }
        }

        return new HashMap<>(counter.cardMap);
    }

    private float getProbability(PyState state, int playerIndex,
                                 Colour colour, int value, Colour knownColour, int knownValue,
                                 Set<Colour> notColour, Set<Integer> notValue, Map<String, Integer> observedMap)
    {
        // Get the probability of this Colour and Value combination for a card, given what we know.
        PyCardCounter counter = new PyCardCounter();

        if (observedMap == null) {
            counter.cardMap = generateObservationMap(state, playerIndex, -1);
        } else {
            counter.cardMap  = new HashMap<>(observedMap);
        }

        // Eliminate Cards that we know it cannot be.
        for (Colour ci : Colour.values()) {
            for (int i = 1; i < 6; i ++)
            {
                if ((knownColour != null && knownColour != ci) || (knownValue > 0 && knownValue != i))
                    counter.set(ci, i, 0);

                if ((notColour != null && notColour.contains(ci)) || (notValue != null && notValue.contains(i)))
                    counter.set(ci, i, 0);
            }
        }

        int cardCount = counter.count(colour, value);
        int totalCount = counter.totalCount();
        if (totalCount == 0)
            return 0.0f;

        return (float) cardCount / (float) totalCount;
    }

    private float getPlayRating(PyState state, Colour colour, int value)
    {
        return state.isCardPlayable(colour, value) ? 1.0f : 0.0f;
    }

    private float getDiscardRating(PyState state, Colour colour, int value)
    {
        return state.getDiscardScore(colour, value);
    }

    private PyCardMatrix getCardMatrix(PyState state, int playerIndex, Colour knownColour, int knownValue,
                                       Set<Colour> notColour, Set<Integer> notValue, Map<String, Integer> observedMap)
    {
        PyCardMatrix matrix = new PyCardMatrix();

        // For each possible card, work out its probability, play and discard rating.
        for (Colour c : Colour.values())
        {
            for (int v = 1; v < 6; v ++)
            {
                PyCardStat stat = new PyCardStat();
                stat.colour = c;
                stat.value = v;
                stat.playRating = getPlayRating(state, c, v);
                stat.discardRating = getDiscardRating(state, c, v);
                stat.probability = getProbability(
                        state, playerIndex, c, v, knownColour, knownValue, notColour, notValue, observedMap);
                matrix.add(stat);
            }
        }

        return matrix;
    }

    // ======================================================================================================
    // Hint Analysis Logic.
    // ======================================================================================================

    private ArrayList<PyHint> getValidHintCommands(PyState state, int playerIndex)
    {
        ArrayList<PyHint> hints = new ArrayList<>();

        int numberOfPlayers = state.originalState.getPlayers().length;
        for (int i = 0; i < numberOfPlayers; i++)
        {
            if (i == playerIndex)
                continue;

            HashSet<Colour> colourMap = new HashSet<>();
            HashSet<Integer> valueMap = new HashSet<>();

            PyCard[] hand = state.hands[i];
            for (PyCard card : hand)
            {
                if (card == null)
                    continue;

                if (!card.hasReceivedColourHint())
                    colourMap.add(card.colour);

                if (!card.hasReceivedValueHint())
                    valueMap.add(card.value);
            }

            for (Colour c : colourMap)
                hints.add(new PyHint(playerIndex, i, c, -1, state));

            for (int v : valueMap)
                hints.add(new PyHint(playerIndex, i, null, v, state));
        }

        for (PyHint hint : hints)
            populateHintRating(state, hint);

        return hints;
    }

    private void populateHintRating(PyState state, PyHint hint)
    {
        PyCard[] hand = state.hands[hint.targetIndex];
        Map<String, Integer> observedMap = generateObservationMap(state, hint.targetIndex, hint.playerIndex);

        for (PyCard card : hand)
        {
            if (card == null)
                continue;

            PyCardMatrix originalMatrix = getCardMatrix(
                    state, hint.targetIndex, card.getObservedColour(), card.getObservedValue(), card.notColour, card.notValue, observedMap);
            PyCardMatrix postMatrix = originalMatrix;

            // Simulate Giving a Colour Hint.
            if (hint.colour != null && hint.colour == card.colour)
            {
                if (!card.hasReceivedColourHint())
                    hint.registerEffect(card, state);

                postMatrix = getCardMatrix(
                        state, hint.targetIndex, hint.colour, card.getObservedValue(), card.notColour, card.notValue, observedMap);
            }

            // Simulate Giving a Value Hint.
            if (hint.value > 0 && hint.value == card.value)
            {
                if (!card.hasReceivedValueHint()) {
                    hint.registerEffect(card, state);
                    if (hint.value == 5)
                        hint.vitalReveal ++;
                }

                postMatrix = getCardMatrix(
                        state, hint.targetIndex, card.getObservedColour(), hint.value, card.notColour, card.notValue, observedMap);
            }

            float playGain = postMatrix.getPlayRating() - originalMatrix.getPlayRating();
            float discardGain = postMatrix.getDiscardRating() - originalMatrix.getDiscardRating();

            if (postMatrix.getPlayRating() > 0.99f && playGain > 0f)
                hint.enablesPlay ++;

            if (postMatrix.getDiscardRating() > 0.99f && discardGain > 0f)
                hint.enablesDiscard ++;

            hint.totalPlayGain += playGain;
            hint.totalDiscardGain += discardGain;
            hint.maxPlayGain = Math.max(hint.maxPlayGain, playGain);
            hint.maxDiscardGain = Math.max(hint.maxDiscardGain, discardGain);
        }
    }

    private PyHint getBestHint(List<PyHint> hints)
    {
        hints.sort(new PyHintComparator());
        return hints.get(hints.size() - 1);
    }
}

// ======================================================================================================
// CLASS: Py Card | More useful hint information stored on this card.
// ======================================================================================================

class PyCard {

    Colour colour = null;
    int value = -1;
    int age = 0;

    boolean sealed = false;

    private int valueHintCounter = 0;
    private int colourHintCounter = 0;

    Set<Colour> notColour = new HashSet<>();
    Set<Integer> notValue = new HashSet<>();

    void receiveColourHint(Colour colour)
    {
        colourHintCounter++;
        this.colour = colour;
    }

    void receiveValueHint(int value)
    {
        valueHintCounter++;
        this.value = value;
    }

    void denyColour(Colour colour)
    {
        notColour.add(colour);
    }
    void denyValue(int value)
    {
        notValue.add(value);
    }

    boolean hasReceivedColourHint()
    {
        return colourHintCounter > 0;
    }
    boolean hasReceivedValueHint()
    {
        return valueHintCounter > 0;
    }

    Colour getObservedColour()
    {
        return hasReceivedColourHint() ? colour : null;
    }

    int getObservedValue()
    {
        return hasReceivedValueHint() ? value : -1;
    }

    String key()
    {
        return PyCardUtil.getKey(colour, value);
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof PyCard))
            return false;

        PyCard card = (PyCard) o;
        return card.colour == colour && card.value == value;
    }

    @Override
    public String toString() {
        String colourString = colour == null ? "??" : colour.toString();
        String valueString = value == -1 ? "??" : String.valueOf(value);
        StringBuilder hintToken = new StringBuilder();
        if (hasReceivedColourHint())
            hintToken.append("C");
        if (hasReceivedValueHint())
            hintToken.append("V");
        return "[" + colourString + " " + valueString + " " + hintToken + "]";
    }
}

// ======================================================================================================
// CLASS: Card Matrix
// ======================================================================================================

class PyCardMatrix {

    private Map<String, PyCardStat> stats = new HashMap<>();
    int handIndex = 0;
    int age = 0;
    float playRatingFactor = 1.0f;

    void add(PyCardStat stat)
    {
        String key = PyCardUtil.getKey(stat.colour, stat.value);
        stats.put(key, stat);
    }

    float getPlayRating()
    {
        float score = 0.0f;
        for (String key : stats.keySet())
        {
            PyCardStat stat = stats.get(key);
            score += stat.probability * stat.playRating;
        }

        if (score < 1.0) {
            score *= playRatingFactor;
            score = Math.min(0.99f, score);
        }

        return score;
    }

    float getDiscardRating()
    {
        float score = 0.0f;
        for (String key : stats.keySet())
        {
            PyCardStat stat = stats.get(key);
            score += stat.probability * stat.discardRating;
        }
        return score;
    }
}

// ======================================================================================================
// CLASS: Frozen State | Use this to assist with building the Bayesian model.
// ======================================================================================================

class PyState {

    PyCard[][] hands;

    // A mapping for card and board state analysis.
    private ArrayList<PyCard> playableCards = new ArrayList<>();
    private Map<String, Boolean> playableCardMap = new HashMap<>();
    private Map<Colour, Integer> playableNumberMap = new HashMap<>();
    private Map<Colour, Boolean> blockedColourMap = new HashMap<>();
    private Map<String, Integer> visibleMap = PyCardCounter.getEmptyMap();
    State originalState;

    PyState(State state) throws IllegalActionException {
        // Rebuild the frozen, information rich state from the game state.
        originalState = state;
        ArrayList<State> stateList = createStateChain(state);

        hands = createHand(state);
        updateActions(stateList, hands);
        calibrateMaps(state);
    }

    // ======================================================================================================
    // Core Utility Functions.
    // ======================================================================================================

    boolean isCardPlayable(PyCard card)
    {
        return playableCardMap.containsKey(card.key());
    }

    boolean isCardPlayable(Colour colour, int value)
    {
        return playableCardMap.containsKey(PyCardUtil.getKey(colour, value));
    }

    float getDiscardScore(Colour colour, int value)
    {
        if (blockedColourMap.get(colour))
            return 1.0f;

        if (value == 5)
            return 0.0f;

        if (playableNumberMap.containsKey(colour) && value < playableNumberMap.get(colour))
            return 1.0f;

        if (visibleMap.get(PyCardUtil.getKey(colour, value)) >= 2)
            return 0.5f;

        if (isCardPlayable(colour, value))
            return 0.0f;

        return 0.3f;
    }

    // ======================================================================================================
    // Functions to build the analysis maps for our agent to use.
    // ======================================================================================================

    private void calibrateMaps(State state)
    {
        calculatePlayableCards(state);
        for (PyCard card : playableCards) {
            playableCardMap.put(card.key(), true);
            playableNumberMap.put(card.colour, card.value);
        }
        calculateBlockedMap(state);
        calculateVisibleMap(state);
    }

    private void calculatePlayableCards(State state)
    {
        // Populate the list of all cards playable this turn.
        for(Colour colour: Colour.values()) {
            Stack<Card> firework = state.getFirework(colour);
            if (firework.size() < 5) {
                PyCard card = new PyCard();
                card.colour = colour;
                card.value = firework.size() + 1;
                playableCards.add(card);
            }
        }
    }

    private void calculateVisibleMap(State state)
    {
        int numberOfPlayers = state.getPlayers().length;

        // Populate the hand with the current known value.
        for (int i = 0; i < numberOfPlayers; i ++)
        {
            Card[] hand = state.getHand(i);
            for (Card card : hand) {
                if (card != null) {
                    String key = PyCardUtil.getKey(card);
                    visibleMap.put(key, visibleMap.get(key) + 1);
                }
            }
        }
    }

    private void calculateBlockedMap(State state)
    {
        // Returns a mapping of Colour to boolean, indicating whether or not this Colour is blocked from playing.

        // Initially no Colours are blocked.
        for(Colour colour: Colour.values())
            blockedColourMap.put(colour, false);

        // For each playable card...
        // Get the total number in the deck.
        // And check if the discard pile has depleted it.

        Map<String, Integer> deckMap = PyCardCounter.getDeckMap();
        for (PyCard card : playableCards) {
            int totalNumber = deckMap.get(card.key());

            for (Card discardedCard : state.getDiscards())
            {
                if (PyCardUtil.getKey(discardedCard).equals(card.key())) {
                    totalNumber--;
                }

                if (totalNumber <= 0)
                    blockedColourMap.put(card.colour, true);
            }
        }
    }

    // ======================================================================================================
    // Functions to recreate the hand and hint state given all previous actions.
    // ======================================================================================================

    private ArrayList<State> createStateChain(State state)
    {
        ArrayList<State> stateList = new ArrayList<>();

        // Add the current state to the list.
        stateList.add(state);

        // Add all previous states to the list.
        while (state.getOrder() > 0) {
            state = state.getPreviousState();
            stateList.add(state);
        }

        return stateList;
    }

    private PyCard[][] createHand(State state)
    {
        int numberOfPlayers = state.getPlayers().length;
        hands = new PyCard[numberOfPlayers][numberOfPlayers > 3 ? 4 : 5];

        // Populate the hand with the current known value.
        for (int i = 0; i < numberOfPlayers; i ++)
        {
            Card[] stateHand = state.getHand(i);
            PyCard[] hand = hands[i];

            for (int j = 0; j < stateHand.length; j ++)
            {
                PyCard pyCard = new PyCard();
                Card stateCard = stateHand[j];
                if (stateCard != null) {
                    // We can see the details of this card.
                    pyCard.colour = stateCard.getColour();
                    pyCard.value = stateCard.getValue();

                } else if (state.getNextPlayer() != i)
                {
                    // This is a card that has been discarded.
                    pyCard = null;
                }

                // Copy the card into our frozen hand.
                hand[j] = pyCard;
            }
        }
        return hands;
    }

    private void updateActions(ArrayList<State> stateList, PyCard[][] hands) throws IllegalActionException {
        // Step through the action chain to update the cards hint state.
        for (State s : stateList) {
            Action action = s.getPreviousAction();
            if (action == null)
                continue;

            updateAge(hands);

            if (action.getType() == ActionType.HINT_COLOUR || action.getType() == ActionType.HINT_VALUE)
                updateHint(hands, action);

            if (action.getType() == ActionType.DISCARD || action.getType() == ActionType.PLAY)
                sealCard(hands, action);
        }
    }

    private void updateAge(PyCard[][] hands)
    {
        for (PyCard[] hand : hands)
        {
            for (PyCard card : hand)
            {
                if (card != null && !card.sealed)
                    card.age ++;
            }
        }
    }

    private void updateHint(PyCard[][] hands, Action action) throws IllegalActionException {
        int playerIndex = action.getHintReceiver();
        boolean[] hintList = action.getHintedCards();

        PyCard[] hand = hands[playerIndex];
        for (int i = 0; i < hand.length; i++)
        {
            PyCard card = hand[i];

            // This hint is irrelevant to us right now.
            if (card == null || card.sealed)
                continue;

            if (hintList[i])
                receiveHint(card, action);
            else
                denyHint(card, action);
        }
    }

    private void receiveHint(PyCard card, Action action) throws IllegalActionException {
        if (action.getType() == ActionType.HINT_COLOUR)
            card.receiveColourHint(action.getColour());
        else
            card.receiveValueHint(action.getValue());
    }

    private void denyHint(PyCard card, Action action) throws IllegalActionException {
        if (action.getType() == ActionType.HINT_COLOUR)
            card.denyColour(action.getColour());
        else
            card.denyValue(action.getValue());
    }

    private void sealCard(PyCard[][] hands, Action action) throws IllegalActionException {
        int playerIndex = action.getPlayer();
        int cardIndex = action.getCard();

        PyCard card = hands[playerIndex][cardIndex];
        if (card != null)
            card.sealed = true;
    }
}

// ======================================================================================================
// CLASS: Card Counter | Use this to keep track of how many cards are still unknown.
// ======================================================================================================

class PyCardCounter {

    // ======================================================================================================
    // Static Methods. Helps to get reference collections.
    // ======================================================================================================

    private static Map<String, Integer> _deckMap;
    private static Map<String, Integer> _emptyMap;

    static Map<String, Integer> getDeckMap()
    {
        // Create the deck map if it didn't exist yet.
        if (_deckMap == null) {
            _deckMap = new HashMap<>();
            Card[] deck = Card.getDeck();
            for (Card card : deck)
            {
                String key = PyCardUtil.getKey(card);
                _deckMap.put(key, _deckMap.getOrDefault(key, 0) + 1);
            }
        }

        // Return a copy of the deck map, if it already exists.
        return new HashMap<>(_deckMap);
    }

    static Map<String, Integer> getEmptyMap()
    {
        // Create the empty map if it didn't exist yet.
        if (_emptyMap == null) {
            _emptyMap = new HashMap<>();
            for (Colour colour : Colour.values())
            {
                for (int v = 1; v < 6; v++)
                {
                    String key = PyCardUtil.getKey(colour, v);
                    _emptyMap.put(key, 0);
                }
            }
        }

        // Return a copy of the empty map, if it already exists.
        return new HashMap<>(_emptyMap);
    }

    // ======================================================================================================
    // Static Utility Functions.
    // ======================================================================================================

    static PyCardCounter newDeckCounter() {
        PyCardCounter counter = new PyCardCounter();
        counter.cardMap = getDeckMap();
        return counter;
    }

    // ======================================================================================================
    // Class Implementation.
    // ======================================================================================================

    Map<String, Integer> cardMap;

    PyCardCounter() {
        cardMap = getEmptyMap();
    }

    void set(Colour colour, int value, int amount)
    {
        set(PyCardUtil.getKey(colour, value), amount);
    }

    private void set(String key, int amount)
    {
        cardMap.put(key, amount);
    }
    void add(Colour colour, int value, int amount)
    {
        add(PyCardUtil.getKey(colour, value), amount);
    }
    private void add(String key, int amount)
    {
        cardMap.put(key, cardMap.get(key) + amount);
    }
    int count(Colour colour, int value)
    {
        return count(PyCardUtil.getKey(colour, value));
    }
    private int count(String key)
    {
        return cardMap.get(key);
    }

    int totalCount()
    {
        // Count the total number of cards tracked in this counter.
        int count = 0;
        for (String key : cardMap.keySet()) {
            count += cardMap.get(key);
        }
        return count;
    }
}

// ======================================================================================================
// CLASS: Hint | Use this to quantify the effectiveness of a hint.
// ======================================================================================================

class PyHint {

    // Hint: Action Commands.
    int targetIndex;
    int playerIndex;
    int value;
    Colour colour;

    // Hint: Value Analysis.
    int enablesPlay = 0;
    int enablesDiscard = 0;
    float totalPlayGain = 0.0f;
    float totalDiscardGain = 0.0f;
    float maxPlayGain = 0.0f;
    float maxDiscardGain = 0.0f;
    int vitalReveal = 0;

    private int distance;
    private int truePlayableCards = 0;

    PyHint(int playerIndex, int targetIndex, Colour colour, int value, PyState state)
    {
        this.playerIndex = playerIndex;
        this.targetIndex = targetIndex;
        this.colour = colour;
        this.value = value;
        distance = 0;

        int i = playerIndex;
        while (i != targetIndex)
        {
            distance ++;
            i ++;

            if (i >= state.originalState.getPlayers().length)
                i = 0;
        }
        distance = state.originalState.getPlayers().length - distance;
    }

    void registerEffect(PyCard card, PyState state)
    {
        // This hint can affect the board state.
        if (state.isCardPlayable(card))
            truePlayableCards ++;
    }

    float getPlayEnablingScore()
    {
        return distance * (enablesPlay > 0 ? 1f : 0);
    }

    float getTruePlayScore()
    {
        return (truePlayableCards > 0 ? 1f : 0);
    }

    float getDiscardEnablingScore()
    {
        return distance * (enablesDiscard > 1 ? 1f : 0);
    }

    float getMaxPlayGainScore()
    {
        return distance * totalPlayGain;
    }

    @Override
    public String toString() {
        String hintSubject = (colour != null) ? colour.toString() : String.valueOf(value);
        return "Hint: [" + hintSubject + " to Player " + targetIndex + "]: " +
                "{" + getPlayEnablingScore() +", " + getTruePlayScore() +", " + getDiscardEnablingScore() + ", "+getMaxPlayGainScore()+ "}";
    }
}

class PyHintComparator implements Comparator<PyHint> {
    public int compare(PyHint o1, PyHint o2) {
        int rPlayEnabling = Float.compare(o1.getPlayEnablingScore(), o2.getPlayEnablingScore());
        if (rPlayEnabling != 0)
            return rPlayEnabling;

        int rTruePlayable = Float.compare(o1.getTruePlayScore(), o2.getTruePlayScore());
        if (rTruePlayable != 0)
            return rTruePlayable;

        int rDiscardEnabling = Float.compare(o1.getDiscardEnablingScore(), o2.getDiscardEnablingScore());
        if (rDiscardEnabling != 0)
            return rDiscardEnabling;

        return Float.compare(o1.getMaxPlayGainScore(), o2.getMaxPlayGainScore());
    }
}

// ======================================================================================================
// CLASS: Card Utils | Tools to turn a card into a String key for our Hashes.
// ======================================================================================================

class PyCardUtil {
    static String getKey(Card card)
    {
        // Get the hash-key for a card for quick map lookups.
        return card.getColour().toString() + card.getValue();
    }

    static String getKey(Colour color, int value)
    {
        // Get the hash-key for a card for quick map lookups.
        return color.toString() + value;
    }
}

// ======================================================================================================
// CLASS: Card Stat | Collect the analytical stats of a card into one place.
// ======================================================================================================

class PyCardStat {
    Colour colour;
    int value;
    float probability;
    float discardRating;
    float playRating;
}

