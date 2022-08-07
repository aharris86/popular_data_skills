import popular_data_skills.dashboard.app as dashboard
import popular_data_skills.config.config as config
import runpy

def main():
    runpy.run_path(path_name=config.DASHBOARD_SCRIPT)

if __name__ == "__main__":
    main()
