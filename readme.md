
# Know My Voice - Singing Contest Scoring System

This project is a scoring system for singing contests, designed to help organizers manage competition rounds, participants, and judges, as well as generate official PDF reports and minutes. Built with Django, the system allows for easy score administration and official document generation.

## Features

- **Participant Management**: Allows creation, viewing, updating, and deletion of participants, along with detailed participant information.
- **Round Management**: Organizes competition rounds with options to assign judges and participants, and to activate or deactivate specific rounds.
- **Judge Scoring**: Each judge can score participants based on three criteria: Rhythm Coupling, Intonation, and Expression.
- **PDF Report Generation**: Allows generation of official reports in PDF format for participation order lists, score summaries, and results.
- **Automated Scoring**: Participant scores are calculated automatically and can be viewed by round.
- **Randomized Order**: Enables random sorting of participants in each round for presentation order.
- **Township Management**: Townships can be registered and managed, associated with each participant.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- pip (Python package manager)
- Django
- WeasyPrint (for PDF generation)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/brygallo/know_my_voice.git
   cd know_my_voice
   ```

2. **Set up the virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   Rename the `.env.example` file to `.env` and configure the necessary settings.

5. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Start the development server**:

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000/`.

## Usage

### Main Functionalities

1. **Participants**:
   - Register, edit, delete, and view participant details.
   - Each participant can have a township assigned, along with contact details and date of birth.

2. **Rounds**:
   - Create and manage competition rounds, with options to activate or deactivate each round.
   - Assign judges and participants to each round.
   - Detailed round view showing the list of participants and their assigned scores.

3. **Judge Scoring**:
   - Judges can evaluate participants in each round based on specific criteria (Rhythm Coupling, Intonation, and Expression).
   - Total scores are calculated automatically and displayed in the round details.

4. **PDF Reports**:
   - Generate PDF reports for results minutes, participant order lists, and final round results.
   - Minutes can only be generated if all judges have evaluated all participants.

5. **Randomized Order**:
   - Function to randomly order participants in each round and establish their presentation order.

### Service Context

The system uses services to build the context data for views and reports:

- **`RoundContextService`**: Provides methods to organize participant information, such as order and scores assigned by judges.

### Township Management

The system allows managing townships, which are assigned to each participant.

## Contribution

To contribute to the project:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/NewFeature`).
3. Make your changes and push them (`git push origin feature/NewFeature`).
4. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
