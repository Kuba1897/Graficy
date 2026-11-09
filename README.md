# Graficy — grafy i ich zastosowania

Program uruchamia się z wiersza poleceń przez `graphs.py`. Obsługuje grafy
nieskierowane oraz grafy skierowane. Wierzchołki są numerowane od `1`.

## Instalacja

```powershell
python -m pip install -r env/requirements_python12.txt
```

Pomoc programu:

```powershell
python graphs.py -h
```

## Składnia ogólna i wspólne opcje

```text
python graphs.py -gh {undirected,directed} -dp OPERACJA [pozostałe opcje]
```

`-gh` / `--graph` wybiera typ grafu: `undirected` albo `directed`.

`-dp` / `--display` wybiera operację. Dostępne operacje zależą od typu grafu
i są opisane niżej.

### `-f FORMAT PLIK`

Wczytuje graf z pliku tekstowego. Format może być jednym z poniższych:

- `auto` — automatyczne rozpoznanie,
- `adj_list` — lista sąsiedztwa,
- `adj_matrix` — macierz sąsiedztwa,
- `inc_matrix` — macierz incydencji,
- `seq` — ciąg stopni grafu; tylko dla grafów nieskierowanych.

```powershell
python graphs.py -gh undirected -dp adj_list `
  -f adj_list test_input\adjacent_list.txt
```

Lista sąsiedztwa ma format:

```text
1. 2 3 6
2. 1 3 4 5
3. 1 2 4 6
```

W grafie skierowanym `1. 2 3` oznacza krawędzie `1 -> 2` i `1 -> 3`;
krawędź powrotna nie jest dodawana automatycznie.

### `-out PLIK`

Zapisuje wynik tekstowy albo obraz grafu. Jest wymagane przez `graph` i `mst`.

```powershell
python graphs.py -gh undirected -dp graph `
  -f adj_list test_input\adjacent_list.txt -out graph.png
```

### `-weights PLIK`

Wczytuje wagi. Każda linia musi mieć format:

```text
źródło cel waga
```

Przykład:

```text
1 2 4
1 3 -2
2 3 3
```

Dla grafu nieskierowanego kolejność końców nie ma znaczenia. Dla grafu
skierowanego `1 2 4` i `2 1 -3` są dwiema różnymi krawędziami.

### `-genweights`

Generuje wagi `1..10` dla grafu nieskierowanego. Wymaga `-out PREFIX` i zapisuje
plik `PREFIX_weights.txt`:

```powershell
python graphs.py -gh undirected -dp dijkstra `
  -f adj_list test_input\adjacent_list.txt -genweights -out graph
```

## Grafy nieskierowane

### Reprezentacje grafu

Lista sąsiedztwa — `-dp adj_list`:

```powershell
python graphs.py -gh undirected -dp adj_list `
  -f adj_list test_input\adjacent_list.txt
```

Macierz sąsiedztwa — `-dp adj_matrix`:

```powershell
python graphs.py -gh undirected -dp adj_matrix `
  -f adj_list test_input\adjacent_list.txt
```

Macierz incydencji — `-dp inc_matrix`:

```powershell
python graphs.py -gh undirected -dp inc_matrix `
  -f adj_list test_input\adjacent_list.txt
```

### Rysowanie — `-dp graph`

```powershell
python graphs.py -gh undirected -dp graph `
  -f adj_list test_input\adjacent_list.txt -out graph.png
```

Z wagami:

```powershell
python graphs.py -gh undirected -dp graph `
  -f adj_list test_input\adjacent_list.txt `
  -weights weights.txt -out weighted_graph.png
```

### Generowanie grafu — `-gen TYP N PARAMETR`

Graf `G(n,p)`, gdzie każda możliwa krawędź ma prawdopodobieństwo `p`:

```powershell
python graphs.py -gh undirected -dp adj_list -gen np 8 0.3
```

Graf z dokładnie `l` krawędziami:

```powershell
python graphs.py -gh undirected -dp adj_list -gen nl 8 12
```

Graf `k`-regularny:

```powershell
python graphs.py -gh undirected -dp adj_list -gen kregular 8 3
```

`-c` wymusza spójność grafu generowanego przez `-gen`:

```powershell
python graphs.py -gh undirected -dp components -gen nl 8 12 -c
```

`-genseq N` generuje graf na podstawie losowego ciągu graficznego:

```powershell
python graphs.py -gh undirected -dp adj_list -genseq 8
```

`-geneuler N` generuje graf z losowym ciągiem przeznaczonym do testowania
cyklu Eulera:

```powershell
python graphs.py -gh undirected -dp euler -geneuler 8
```

`-rand LICZBA` wykonuje podaną liczbę losowych zamian par krawędzi:

```powershell
python graphs.py -gh undirected -dp adj_list `
  -f adj_list test_input\adjacent_list.txt -rand 10
```

### Składowe spójne — `-dp components`

```powershell
python graphs.py -gh undirected -dp components `
  -f adj_list test_input\adjacent_list.txt
```

Opcjonalne `-out components.png` zapisuje obraz z pokolorowanymi składowymi.

### Cykl Eulera — `-dp euler`

```powershell
python graphs.py -gh undirected -dp euler `
  -f adj_list test_input\adjacent_list.txt
```

`-out euler.png` zapisuje wizualizację znalezionego cyklu.

### Cykl Hamiltona — `-dp hamilton`

```powershell
python graphs.py -gh undirected -dp hamilton `
  -f adj_list test_input\adjacent_list.txt
```

`-out hamilton.png` zapisuje wizualizację znalezionego cyklu.

### Dijkstra — `-dp dijkstra -dij START`

Oblicza najkrótsze ścieżki od `START`. Wymaga pliku nieujemnych wag:

```powershell
python graphs.py -gh undirected -dp dijkstra -dij 1 `
  -f adj_list test_input\adjacent_list.txt -weights weights.txt
```

### Wszystkie odległości — `-dp dijkstra_all`

```powershell
python graphs.py -gh undirected -dp dijkstra_all `
  -f adj_list test_input\adjacent_list.txt -weights weights.txt
```

`-out distances.txt` zapisuje macierz odległości.

### Centrum — `-dp center`

```powershell
python graphs.py -gh undirected -dp center `
  -f adj_list test_input\adjacent_list.txt -weights weights.txt
```

Zwraca wierzchołek o najmniejszej sumie odległości do pozostałych.

### Centrum minimaksowe — `-dp minimax_center`

```powershell
python graphs.py -gh undirected -dp minimax_center `
  -f adj_list test_input\adjacent_list.txt -weights weights.txt
```

Zwraca wierzchołek, którego najdalszy wierzchołek jest możliwie blisko.

### Minimalne drzewo rozpinające — `-dp mst`

```powershell
python graphs.py -gh undirected -dp mst `
  -f adj_list test_input\adjacent_list.txt `
  -weights weights.txt -out mst.png
```

Program wypisuje krawędzie drzewa, łączną wagę oraz zapisuje obraz.

## Grafy skierowane

Dla grafów skierowanych dostępne są: `adj_list`, `scc`, `bellman_ford` i
`johnson`.

### Lista sąsiedztwa — `-dp adj_list`

```powershell
python graphs.py -gh directed -dp adj_list `
  -f adj_list test_input\directed_graph.txt
```

### Losowy digraf `G(n,p)` — `-gen np N P`

`N` to liczba wierzchołków, a `P` to prawdopodobieństwo utworzenia każdej
uporządkowanej krawędzi z zakresu `0..1`:

```powershell
python graphs.py -gh directed -dp adj_list -gen np 8 0.3
```

### Silnie spójne składowe — `-dp scc`

Uruchamia algorytm Kosaraju:

```powershell
python graphs.py -gh directed -dp scc `
  -f adj_list test_input\directed_graph.txt
```

### Bellman-Ford — `-dp bellman_ford -dij START -weights PLIK`

Oblicza najkrótsze ścieżki od `START`, obsługuje wagi ujemne i zgłasza błąd
przy osiągalnym ujemnym cyklu:

```powershell
python graphs.py -gh directed -dp bellman_ford -dij 1 `
  -f adj_list test_input\directed_graph.txt `
  -weights test_input\directed_weights.txt
```

### Johnson — `-dp johnson -weights PLIK`

Oblicza odległości pomiędzy wszystkimi parami wierzchołków:

```powershell
python graphs.py -gh directed -dp johnson `
  -f adj_list test_input\directed_graph.txt `
  -weights test_input\directed_weights.txt
```

Może działać z ujemnymi wagami, ale graf nie może zawierać ujemnego cyklu.

## Przykładowe pliki

- `test_input\adjacent_list.txt` — graf nieskierowany,
- `test_input\directed_graph.txt` — graf skierowany,
- `test_input\directed_weights.txt` — wagi kierunkowe.

## Uwagi

Grafy nieskierowane korzystają z `undirectedGraphsUtils.py`, a skierowane z
`directedGraphsUtils.py`. W grafie skierowanym krawędzie `(1,2)` i `(2,1)` są
różne. Dla ujemnych wag używane są Bellman-Ford i Johnson; Dijkstra wymaga wag
nieujemnych.
