"""
Script de test pour valider le backend Flask
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_health():
    """Test de santé du serveur"""
    print("\n1. Test Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("   ✓ Backend accessible")
            print(f"   Message: {response.json()['message']}")
            return True
        else:
            print(f"   ✗ Erreur: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ✗ Impossible de se connecter au backend")
        print("   Assurez-vous que le serveur Flask est lancé (python backend/app.py)")
        return False
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
        return False

def test_compounds():
    """Test de la liste des composés"""
    print("\n2. Test Liste des Composés...")
    try:
        response = requests.get(f"{BASE_URL}/compounds", timeout=5)
        if response.status_code == 200:
            compounds = response.json()['compounds']
            print(f"   ✓ {len(compounds)} composés disponibles")
            print(f"   Exemples: {', '.join([c['name'] for c in compounds[:3]])}")
            return True
        else:
            print(f"   ✗ Erreur: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
        return False

def test_simulation():
    """Test d'une simulation complète"""
    print("\n3. Test Simulation BTX...")

    simulation_data = {
        "compounds": ["benzene", "toluene", "o-xylene"],
        "compositions": [0.33, 0.33, 0.34],
        "flow_rate": 100.0,
        "pressure": 101325,
        "recovery_lk": 0.95,
        "recovery_hk": 0.95,
        "reflux_factor": 1.3,
        "feed_quality": 1.0,
        "efficiency": 0.70
    }

    try:
        response = requests.post(
            f"{BASE_URL}/simulate",
            json=simulation_data,
            timeout=30
        )

        if response.status_code == 200:
            results = response.json()
            if results['success']:
                print("   ✓ Simulation réussie")
                r = results['results']
                print(f"   • N_min: {r['N_min']:.2f} plateaux")
                print(f"   • R_min: {r['R_min']:.3f}")
                print(f"   • N_réel: {r['N_real']} plateaux")
                print(f"   • Plateau alimentation: {r['feed_stage']}")
                print(f"   • Débit distillat: {r['flow_distillate']:.2f} kmol/h")
                print(f"   • Débit résidu: {r['flow_bottom']:.2f} kmol/h")
                return True
            else:
                print(f"   ✗ Erreur simulation: {results.get('error', 'Unknown')}")
                return False
        else:
            print(f"   ✗ Erreur HTTP: {response.status_code}")
            print(f"   Message: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
        return False

def test_compound_properties():
    """Test des propriétés d'un composé"""
    print("\n4. Test Propriétés du Benzène...")

    try:
        response = requests.post(
            f"{BASE_URL}/compound-properties",
            json={"compound_id": "benzene"},
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            if data['success']:
                props = data['properties']
                print("   ✓ Propriétés récupérées")
                print(f"   • Tb: {props['Tb']:.2f} °C")
                print(f"   • Tc: {props['Tc']:.2f} °C")
                print(f"   • Pc: {props['Pc']:.2f} bar")
                print(f"   • MW: {props['MW']:.2f} g/mol")
                return True
            else:
                print(f"   ✗ Erreur: {data.get('error', 'Unknown')}")
                return False
        else:
            print(f"   ✗ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print("=" * 60)
    print("  TESTS DU BACKEND FLASK - SIMULATEUR DE DISTILLATION")
    print("=" * 60)

    results = []

    # Test 1: Health check
    results.append(test_health())

    if not results[0]:
        print("\n⚠️  Le backend n'est pas accessible. Lancez-le avec:")
        print("   cd backend && python app.py")
        return

    # Test 2: Composés
    results.append(test_compounds())

    # Test 3: Propriétés
    results.append(test_compound_properties())

    # Test 4: Simulation complète
    results.append(test_simulation())

    # Résumé
    print("\n" + "=" * 60)
    print("  RÉSUMÉ DES TESTS")
    print("=" * 60)

    total = len(results)
    passed = sum(results)

    print(f"\n  Tests réussis: {passed}/{total}")

    if passed == total:
        print("\n  ✓ Tous les tests sont passés avec succès!")
        print("  Le backend est opérationnel.")
    else:
        print(f"\n  ⚠️  {total - passed} test(s) échoué(s)")
        print("  Vérifiez les erreurs ci-dessus.")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    run_all_tests()
