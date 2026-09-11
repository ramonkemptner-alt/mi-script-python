import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator


class QuantumAntiRegister:
    """Clase que gestiona un registro de N qubits y automatiza

    la creación de su estado "Anti-Qubit" (operación inversa).
    """

    def __init__(self, num_qubits: int, name: str = "qreg"):
        """Inicializa el registro cuántico de N qubits."""
        self.num_qubits = num_qubits
        self.qr = QuantumRegister(num_qubits, name=name)
        self.cr = ClassicalRegister(num_qubits, name="medicion")

        # Circuito donde aplicaremos las transformaciones directas
        self.forward_circuit = QuantumCircuit(self.qr)

    def apply_hadamard(self, qubit_index: int):
        """Aplica una puerta Hadamard al qubit especificado."""
        self.forward_circuit.h(self.qr[qubit_index])

    def apply_rotation_x(self, qubit_index: int, theta: float):
        """Aplica una rotación en X con ángulo theta al qubit especificado."""
        self.forward_circuit.rx(theta, self.qr[qubit_index])

    def apply_cnot(self, control_index: int, target_index: int):
        """Aplica una puerta CNOT (Entrelazamiento) entre dos qubits."""
        self.forward_circuit.cx(
            self.qr[control_index], self.qr[target_index]
        )

    def get_anti_circuit(self) -> QuantumCircuit:
        """Genera y retorna automáticamente el 'Anti-Circuito' (Inverso Hermitiano).

        invierte el orden de las puertas y aplica la adjunta de cada una.
        """
        # Utiliza el método nativo inverse() de Qiskit para generar la transformación opuesta
        return self.forward_circuit.inverse()

    def build_full_circuit(
        self, apply_anti: bool = True, measure: bool = True
    ) -> QuantumCircuit:
        """Ensambla el circuito completo:

        [Transformación Original] + [Anti-Qubit Inverso] + [Medición]
        """
        full_circuit = QuantumCircuit(self.qr, self.cr)

        # 1. Agregar transformaciones directas
        full_circuit.compose(self.forward_circuit, inplace=True)
        full_circuit.barrier()

        # 2. Agregar la inversión (Anti-Qubit) si se solicita
        if apply_anti:
            anti_circuit = self.get_anti_circuit()
            full_circuit.compose(anti_circuit, inplace=True)
            full_circuit.barrier()

        # 3. Agregar medición clásica al final
        if measure:
            full_circuit.measure(self.qr, self.cr)

        return full_circuit

    def simulate(self, apply_anti: bool = True, shots: int = 1000) -> dict:
        """Ejecuta la simulación en Qiskit Aer y devuelve el conteo de resultados."""
        circuit = self.build_full_circuit(
            apply_anti=apply_anti, measure=True
        )

        simulator = AerSimulator()
        job = simulator.run(circuit, shots=shots)
        result = job.result()
        return result.get_counts()


# ==========================================
# EJEMPLO DE USO / DEMOSTRACIÓN
# ==========================================
if __name__ == "__main__":
    N_QUBITS = 3
    print(f"=== INICIANDO REGISTRO DE {N_QUBITS} QUBITS Y ANTI-QUBITS ===")

    # 1. Instanciar la clase para 3 qubits
    qsystem = QuantumAntiRegister(num_qubits=N_QUBITS)

    # 2. Crear un estado entrelazado complejo (Ejemplo: Estado GHZ + Rotaciones)
    print("\nApplying transformations to quantum state...")
    qsystem.apply_hadamard(0)  # Superposición en Q0
    qsystem.apply_cnot(0, 1)  # Entrelaza Q0 -> Q1
    qsystem.apply_cnot(1, 2)  # Entrelaza Q1 -> Q2
    qsystem.apply_rotation_x(2, np.pi / 4)  # Rotación arbitraria en Q2

    # 3. Simulación SIN Anti-Qubit (Para ver la distribución cuántica)
    counts_without_anti = qsystem.simulate(apply_anti=False)
    print(
        f"Resultados SIN Anti-Qubit (Estado complejo): {counts_without_anti}"
    )

    # 4. Simulación CON Anti-Qubit (Cancelación total del estado)
    counts_with_anti = qsystem.simulate(apply_anti=True)
    print(
        f"Resultados CON Anti-Qubit (Estado colapsado): {counts_with_anti}"
    )

    # 5. Visualizar el circuito completo en texto
    print("\nVisualización del Circuito Completo:")
    print(qsystem.build_full_circuit(apply_anti=True).draw(output="text"))

    # Validación
    expected_state = "0" * N_QUBITS
    if counts_with_anti.get(expected_state, 0) == 1000:
        print(
            f"\n¡Éxito! El Anti-Qubit de {N_QUBITS} qubits canceló el registro y devolvió todos a |{expected_state}>."
        )