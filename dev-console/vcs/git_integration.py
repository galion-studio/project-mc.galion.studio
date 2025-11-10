"""
Git Integration Module
Version control integration for mod management
"""

import git
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime

from config import SERVER_MODS_DIR, PROJECT_ROOT


class GitIntegration:
    """
    Git integration for version control.
    Simple, powerful, reliable.
    """
    
    def __init__(self, repo_path: Path = PROJECT_ROOT):
        self.repo_path = repo_path
        self.repo = None
        self.initialize_repo()
    
    def initialize_repo(self):
        """Initialize or open Git repository"""
        try:
            # Try to open existing repo
            self.repo = git.Repo(self.repo_path)
        except git.InvalidGitRepositoryError:
            # Initialize new repo
            try:
                self.repo = git.Repo.init(self.repo_path)
                print(f"[Git] Initialized repository at {self.repo_path}")
            except Exception as e:
                print(f"[Git] Error initializing repository: {e}")
                self.repo = None
        except Exception as e:
            print(f"[Git] Error: {e}")
            self.repo = None
    
    def is_initialized(self) -> bool:
        """Check if Git repo is initialized"""
        return self.repo is not None
    
    def get_status(self) -> Dict:
        """Get repository status"""
        if not self.is_initialized():
            return {
                "initialized": False,
                "error": "Repository not initialized"
            }
        
        try:
            changed_files = [item.a_path for item in self.repo.index.diff(None)]
            untracked_files = self.repo.untracked_files
            staged_files = [item.a_path for item in self.repo.index.diff("HEAD")]
            
            return {
                "initialized": True,
                "branch": self.repo.active_branch.name,
                "changed_files": changed_files,
                "untracked_files": untracked_files,
                "staged_files": staged_files,
                "clean": len(changed_files) == 0 and len(untracked_files) == 0
            }
        except Exception as e:
            return {
                "initialized": True,
                "error": str(e)
            }
    
    def commit_mod(self, mod_file: Path, message: Optional[str] = None) -> bool:
        """
        Commit a mod file to repository.
        
        Args:
            mod_file: Path to mod file
            message: Commit message (auto-generated if None)
        
        Returns:
            True if successful
        """
        if not self.is_initialized():
            print("[Git] Repository not initialized")
            return False
        
        try:
            # Make path relative to repo root
            rel_path = mod_file.relative_to(self.repo_path)
            
            # Add file to staging
            self.repo.index.add([str(rel_path)])
            
            # Generate commit message if not provided
            if message is None:
                message = f"Update mod: {mod_file.name}"
            
            # Commit
            self.repo.index.commit(message)
            
            print(f"[Git] Committed: {rel_path}")
            return True
        
        except Exception as e:
            print(f"[Git] Error committing file: {e}")
            return False
    
    def commit_all_mods(self, message: Optional[str] = None) -> bool:
        """
        Commit all mod files in server-mods directory.
        
        Args:
            message: Commit message
        
        Returns:
            True if successful
        """
        if not self.is_initialized():
            return False
        
        try:
            # Add all .jar files in server-mods
            mod_files = list(SERVER_MODS_DIR.glob("*.jar"))
            
            if not mod_files:
                print("[Git] No mod files to commit")
                return False
            
            # Add files
            for mod_file in mod_files:
                rel_path = mod_file.relative_to(self.repo_path)
                self.repo.index.add([str(rel_path)])
            
            # Generate commit message if not provided
            if message is None:
                message = f"Update mods: {len(mod_files)} files"
            
            # Commit
            self.repo.index.commit(message)
            
            print(f"[Git] Committed {len(mod_files)} mod files")
            return True
        
        except Exception as e:
            print(f"[Git] Error committing mods: {e}")
            return False
    
    def get_commit_history(self, file_path: Optional[Path] = None, limit: int = 10) -> List[Dict]:
        """
        Get commit history.
        
        Args:
            file_path: Specific file to get history for (or None for all)
            limit: Maximum number of commits to return
        
        Returns:
            List of commit information
        """
        if not self.is_initialized():
            return []
        
        try:
            commits = []
            
            # Get commits
            if file_path:
                rel_path = file_path.relative_to(self.repo_path)
                commit_iter = self.repo.iter_commits(paths=str(rel_path), max_count=limit)
            else:
                commit_iter = self.repo.iter_commits(max_count=limit)
            
            for commit in commit_iter:
                commits.append({
                    "hash": commit.hexsha[:8],
                    "full_hash": commit.hexsha,
                    "message": commit.message.strip(),
                    "author": commit.author.name,
                    "date": datetime.fromtimestamp(commit.committed_date).isoformat(),
                    "files": list(commit.stats.files.keys())
                })
            
            return commits
        
        except Exception as e:
            print(f"[Git] Error getting commit history: {e}")
            return []
    
    def rollback_to_commit(self, commit_hash: str, file_path: Optional[Path] = None) -> bool:
        """
        Rollback to a specific commit.
        
        Args:
            commit_hash: Commit hash to rollback to
            file_path: Specific file to rollback (or None for all)
        
        Returns:
            True if successful
        """
        if not self.is_initialized():
            return False
        
        try:
            if file_path:
                # Rollback specific file
                rel_path = file_path.relative_to(self.repo_path)
                self.repo.git.checkout(commit_hash, str(rel_path))
                print(f"[Git] Rolled back {rel_path} to {commit_hash}")
            else:
                # Rollback entire repo
                self.repo.git.reset('--hard', commit_hash)
                print(f"[Git] Rolled back repository to {commit_hash}")
            
            return True
        
        except Exception as e:
            print(f"[Git] Error rolling back: {e}")
            return False
    
    def create_tag(self, tag_name: str, message: Optional[str] = None) -> bool:
        """
        Create a Git tag (release).
        
        Args:
            tag_name: Name of the tag (e.g., "v1.0.0")
            message: Tag message
        
        Returns:
            True if successful
        """
        if not self.is_initialized():
            return False
        
        try:
            if message:
                self.repo.create_tag(tag_name, message=message)
            else:
                self.repo.create_tag(tag_name)
            
            print(f"[Git] Created tag: {tag_name}")
            return True
        
        except Exception as e:
            print(f"[Git] Error creating tag: {e}")
            return False
    
    def get_tags(self) -> List[str]:
        """Get all tags"""
        if not self.is_initialized():
            return []
        
        try:
            return [tag.name for tag in self.repo.tags]
        except Exception as e:
            print(f"[Git] Error getting tags: {e}")
            return []
    
    def push_to_remote(self, remote_name: str = "origin", branch: Optional[str] = None) -> bool:
        """
        Push commits to remote repository.
        
        Args:
            remote_name: Name of remote (default: origin)
            branch: Branch to push (default: current branch)
        
        Returns:
            True if successful
        """
        if not self.is_initialized():
            return False
        
        try:
            if branch is None:
                branch = self.repo.active_branch.name
            
            origin = self.repo.remote(remote_name)
            origin.push(branch)
            
            print(f"[Git] Pushed {branch} to {remote_name}")
            return True
        
        except Exception as e:
            print(f"[Git] Error pushing to remote: {e}")
            return False
    
    def pull_from_remote(self, remote_name: str = "origin", branch: Optional[str] = None) -> bool:
        """
        Pull commits from remote repository.
        
        Args:
            remote_name: Name of remote (default: origin)
            branch: Branch to pull (default: current branch)
        
        Returns:
            True if successful
        """
        if not self.is_initialized():
            return False
        
        try:
            if branch is None:
                branch = self.repo.active_branch.name
            
            origin = self.repo.remote(remote_name)
            origin.pull(branch)
            
            print(f"[Git] Pulled {branch} from {remote_name}")
            return True
        
        except Exception as e:
            print(f"[Git] Error pulling from remote: {e}")
            return False
    
    def get_diff(self, commit1: Optional[str] = None, commit2: Optional[str] = None) -> str:
        """
        Get diff between commits.
        
        Args:
            commit1: First commit (default: HEAD)
            commit2: Second commit (default: working directory)
        
        Returns:
            Diff string
        """
        if not self.is_initialized():
            return ""
        
        try:
            if commit1 and commit2:
                diff = self.repo.git.diff(commit1, commit2)
            elif commit1:
                diff = self.repo.git.diff(commit1)
            else:
                diff = self.repo.git.diff()
            
            return diff
        
        except Exception as e:
            print(f"[Git] Error getting diff: {e}")
            return ""


# Singleton instance
_git_integration = None


def get_git() -> GitIntegration:
    """Get Git integration singleton"""
    global _git_integration
    if _git_integration is None:
        _git_integration = GitIntegration()
    return _git_integration


# Test function
if __name__ == "__main__":
    print("="*50)
    print("  GIT INTEGRATION TEST")
    print("="*50)
    print()
    
    git_int = get_git()
    
    # Check status
    print("Repository status:")
    status = git_int.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    print()
    
    # Get commit history
    print("Recent commits:")
    commits = git_int.get_commit_history(limit=5)
    for commit in commits:
        print(f"  {commit['hash']} - {commit['message'][:50]} ({commit['author']})")
    print()
    
    # Get tags
    print("Tags:")
    tags = git_int.get_tags()
    for tag in tags:
        print(f"  {tag}")
    
    if not tags:
        print("  (no tags)")
    
    print("\nDone!")

