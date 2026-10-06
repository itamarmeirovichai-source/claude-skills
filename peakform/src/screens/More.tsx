import { Item, PageHead, Section } from '../ui/components';
import { useSettings } from '../ui/state';
import { ScheduleScreen, CalendarScreen, SabbathSettingsScreen, SettingsScreen, SupplementsScreen, LockSettingsScreen, PlanEditorScreen, CustomExerciseScreen } from './MoreSettings';
import { AthleteScreen, GoalsScreen, SportScreen } from './Athlete';
import { DataScreen, RecommendationScreen } from './MoreData';
import { AttributionScreen, SourcesScreen, PrivacyScreen, SafetyScreen, AboutScreen, InstallScreen } from './MoreInfo';
import { navigate } from '../ui/router';
import { useEffect } from 'react';

export function MoreScreen() {
  const s = useSettings();
  return (
    <div data-testid="more">
      <PageHead title="More" eyebrow={s.appName} />
      <Section title="Plan and schedule">
        <div className="group">
          <Item title="Schedule and reminders" sub="Session times and reminder times" to="/more/schedule" testId="more-schedule" />
          <Item title="Calendar export" sub="Reminders with alarms for Apple Calendar" to="/more/calendar" testId="more-calendar" />
          <Item title="Sabbath Mode" sub={s.sabbath.enabled ? `On, Friday ${s.sabbath.mode === 'manual' ? s.sabbath.fridayStart : 'from sunset'} to Saturday night` : 'Off'} to="/more/sabbath" testId="more-sabbath" />
          <Item title="Your profile" sub="Wrist, home space, school sport, supplements, weighing" to="/more/athlete" testId="more-athlete" />
          <Item title="Goals and reviews" sub="Your aspirations, reviewed targets, and the talk with a parent" to="/more/goals" testId="more-goals" />
          <Item title="School sport" sub="Practices and games count toward the weekly load" to="/more/sport" testId="more-sport" />
          <Item title="Choose your exercises" sub="Your favourite exercise for each muscle head" to="/program" testId="more-program" />
          <Item title="Edit the training plan" sub="Saved as a new version. History keeps the original." to="/more/plan" />
        </div>
      </Section>
      <Section title="Library">
        <div className="group">
          <Item title="Exercises" to="/library" />
          <Item title="Recipes" to="/recipes" />
          <Item title="Meal preparation" to="/prep" />
          <Item title="Supplements" sub="Creatine, calcium, omega 3" to="/more/supplements" />
        </div>
      </Section>
      <Section title="Your data">
        <div className="group">
          <Item title="Backup, export, and import" sub="Everything stays on this phone until you export it" to="/more/data" testId="more-data" />
          <Item title="Import a recommendation" sub="Review every change before it applies" to="/more/recommendation" />
          <Item title="App lock" sub={s.lock.enabled ? 'On' : 'Off'} to="/more/lock" />
          <Item title="Privacy" to="/more/privacy" />
        </div>
      </Section>
      <Section title="Guidance">
        <div className="group">
          <Item title="Safety" sub="Pain, warning signs, and when to tell a parent" to="/more/safety" testId="more-safety" />
          <Item title="Research sources" to="/more/sources" />
          <Item title="Media attribution" to="/more/attribution" />
          <Item title="Install on iPhone" to="/more/install" />
        </div>
      </Section>
      <Section title="App">
        <div className="group">
          <Item title="Settings" sub="Theme, units, rest timer, equipment, profile" to="/more/settings" testId="more-settings" />
          <Item title="About" to="/more/about" />
        </div>
      </Section>
    </div>
  );
}

export function MoreSubScreen({ page, next = null }: { page: string; next?: string | null }) {
  switch (page) {
    case 'schedule':
      return <ScheduleScreen />;
    case 'calendar':
      return <CalendarScreen />;
    case 'sabbath':
      return <SabbathSettingsScreen />;
    case 'settings':
      return <SettingsScreen />;
    case 'targets':
      return <Redirect to="/more/goals" />;
    case 'athlete':
      return <AthleteScreen next={next} />;
    case 'goals':
      return <GoalsScreen />;
    case 'sport':
      return <SportScreen />;
    case 'supplements':
      return <SupplementsScreen />;
    case 'lock':
      return <LockSettingsScreen />;
    case 'plan':
      return <PlanEditorScreen />;
    case 'custom-exercise':
      return <CustomExerciseScreen />;
    case 'data':
      return <DataScreen />;
    case 'recommendation':
      return <RecommendationScreen />;
    case 'attribution':
      return <AttributionScreen />;
    case 'sources':
      return <SourcesScreen />;
    case 'privacy':
      return <PrivacyScreen />;
    case 'safety':
      return <SafetyScreen />;
    case 'about':
      return <AboutScreen />;
    case 'install':
      return <InstallScreen />;
    case 'library':
      return <Redirect to="/library" />;
    default:
      return <MoreScreen />;
  }
}

function Redirect({ to }: { to: string }) {
  useEffect(() => navigate(to, { replace: true }), [to]);
  return null;
}
