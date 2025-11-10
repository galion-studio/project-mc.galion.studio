# Contributing to Project Titan

First off, thank you for considering contributing to Project Titan! 🎉

We're building something revolutionary - a Minecraft server that can handle 20,000+ concurrent players. Your contribution, no matter how small, helps us get closer to that goal.

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Commit Guidelines](#commit-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Testing](#testing)

## Code of Conduct

This project and everyone participating in it is governed by respect, transparency, and collaboration:

- **Be respectful** - Treat everyone with respect
- **Be transparent** - Document your decisions and changes
- **Be collaborative** - Work together, share knowledge
- **Be focused** - Keep discussions on topic and productive
- **Be patient** - Remember this is a volunteer effort

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating a bug report:
1. Check the [existing issues](https://github.com/galion-studio/project-mc.galion.studio/issues)
2. Check the [troubleshooting guide](docs/DEPLOYMENT.md#troubleshooting)
3. Gather information about the bug

**Good Bug Report Includes:**
- Clear title and description
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Java version, etc.)
- Logs and error messages
- Screenshots if relevant

### ✨ Suggesting Features

We love feature suggestions! Please:
1. Check if it's already suggested
2. Explain the problem it solves
3. Describe your proposed solution
4. Consider alternatives you've thought about

### 🔧 Code Contributions

Areas we need help with:

**High Priority:**
- Core server implementation (Paper/Forge bridge)
- Proxy layer development
- Database integration
- Performance optimization

**Medium Priority:**
- Monitoring dashboard
- Auto-scaling logic
- Plugin/mod templates
- Documentation improvements

**Good First Issues:**
- Bug fixes
- Code documentation
- Test coverage
- Configuration improvements

Look for issues labeled:
- `good-first-issue` - Good for newcomers
- `help-wanted` - We need help with this
- `enhancement` - New features
- `bug` - Something isn't working

## Development Setup

### Prerequisites

- **Java 17+** (OpenJDK or Oracle)
- **Docker & Docker Compose**
- **Git**
- **IDE**: IntelliJ IDEA (recommended) or Eclipse
- **PostgreSQL** (for database development)
- **Redis** (for caching layer development)

### Setup Steps

```bash
# 1. Fork and clone
git clone https://github.com/YOUR-USERNAME/project-mc.galion.studio.git
cd project-mc.galion.studio

# 2. Add upstream remote
git remote add upstream https://github.com/galion-studio/project-mc.galion.studio.git

# 3. Copy environment config
cp .env.example .env
# Edit .env with your local settings

# 4. Build the project
./gradlew clean build

# 5. Start development environment
docker-compose up -d postgres redis

# 6. Run tests
./gradlew test

# 7. Import into IDE
# IntelliJ: File -> Open -> select build.gradle.kts
# Eclipse: File -> Import -> Gradle Project
```

### Project Structure

```
titan-common/        - Shared utilities (good starting point)
titan-database/      - Database layer
titan-redis/         - Redis integration
titan-core/          - Core server (complex, Paper/Forge)
titan-proxy/         - Proxy layer (Velocity-based)
titan-api/           - Public APIs
examples/            - Example plugins/mods
```

## Coding Standards

### Java Style Guide

We follow the [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) with minor modifications:

- **Indentation**: 4 spaces (not tabs)
- **Line length**: 120 characters max
- **Braces**: K&R style (opening brace on same line)
- **Comments**: Javadoc for public APIs, inline for complex logic

### Code Quality

- ✅ Write clean, readable code
- ✅ Keep methods focused and small (<50 lines)
- ✅ Use meaningful variable names
- ✅ Add comments for complex logic
- ✅ Handle errors properly (don't swallow exceptions)
- ✅ Follow DRY (Don't Repeat Yourself)
- ✅ Use appropriate design patterns

### Example

```java
/**
 * Retrieves player data from cache or database
 * 
 * This method first checks Redis cache for performance.
 * If not found, it fetches from PostgreSQL and caches the result.
 * 
 * @param uuid Player UUID
 * @return PlayerData object, or null if player doesn't exist
 */
public PlayerData getPlayerData(UUID uuid) {
    // Try cache first (fast path)
    String cached = redisManager.get("player:" + uuid);
    if (cached != null) {
        return PlayerData.fromJson(cached);
    }
    
    // Cache miss - query database
    PlayerData data = databaseManager.executeQuery(
        "SELECT * FROM players WHERE uuid = ?",
        rs -> rs.next() ? PlayerData.fromResultSet(rs) : null,
        uuid
    );
    
    // Cache for next time (if found)
    if (data != null) {
        redisManager.setWithExpiry("player:" + uuid, data.toJson(), 3600);
    }
    
    return data;
}
```

### Documentation

- **All public APIs** must have Javadoc
- **Complex algorithms** need explanation comments
- **Configuration options** should be documented
- **Update README.md** if you change user-facing features

## Commit Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, etc.

### Examples

```
feat(proxy): add player routing algorithm

Implemented smart player routing that considers:
- Server load (CPU, memory, TPS)
- Player friends (social clustering)
- Geographic location (latency)

Closes #42
```

```
fix(database): prevent connection pool exhaustion

Added maximum wait time and better error handling
for database connection acquisition.

Fixes #123
```

```
docs(architecture): update scaling strategy

Added section on predictive auto-scaling and
cost optimization strategies.
```

## Pull Request Process

### Before Submitting

1. ✅ **Update your branch** with latest upstream changes
2. ✅ **Run tests** and ensure they pass (`./gradlew test`)
3. ✅ **Run linter** if applicable
4. ✅ **Update documentation** if you changed APIs or configs
5. ✅ **Test manually** - actually run the code
6. ✅ **Write descriptive commit messages**

### PR Template

```markdown
## Description
Brief description of what this PR does

## Motivation
Why is this change needed?

## Changes
- List of changes made
- Be specific

## Testing
How did you test this?
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manually tested in dev environment

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-reviewed my code
- [ ] Commented complex sections
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Tests pass locally
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **At least one maintainer** must review
3. **Address feedback** promptly and professionally
4. **Squash commits** if requested
5. **Maintainer will merge** when approved

### After Merge

- Your PR will be included in the next release
- You'll be added to contributors list
- Share your contribution! (with credit to project)

## Testing

### Running Tests

```bash
# All tests
./gradlew test

# Specific module
./gradlew :titan-common:test

# With coverage
./gradlew test jacocoTestReport

# Integration tests
./gradlew integrationTest
```

### Writing Tests

- **Unit tests** for individual methods/classes
- **Integration tests** for component interaction
- **Load tests** for performance validation
- Aim for **80%+ code coverage**

Example test:

```java
@Test
void testPlayerDataSerialization() {
    // Arrange
    UUID uuid = UUID.randomUUID();
    PlayerData data = PlayerData.create(uuid, "TestPlayer");
    data.setRank("admin");
    data.setBalance(1000.0);
    
    // Act
    String json = data.toJson();
    PlayerData deserialized = PlayerData.fromJson(json);
    
    // Assert
    assertEquals(uuid, deserialized.getUuid());
    assertEquals("TestPlayer", deserialized.getUsername());
    assertEquals("admin", deserialized.getRank());
    assertEquals(1000.0, deserialized.getBalance());
}
```

## Performance Considerations

When contributing, keep in mind:

- **We're targeting 20k players** - scalability is critical
- **Avoid blocking operations** in main thread
- **Use connection pooling** for database/Redis
- **Cache frequently accessed data**
- **Profile before optimizing** (measure, don't guess)
- **Document performance characteristics** of new code

## Questions?

- **GitHub Discussions**: For general questions
- **GitHub Issues**: For specific problems
- **Discord**: [Join our server](https://discord.gg/your-invite) (coming soon)
- **Email**: titan@galion.studio

## Recognition

Contributors will be:
- Listed in **CONTRIBUTORS.md**
- Credited in **release notes**
- Mentioned in **documentation** where relevant
- Given our eternal gratitude 🙏

---

**Thank you for contributing to Project Titan!** Together, we're building something amazing. 🚀

*"The best way to predict the future is to build it."*

